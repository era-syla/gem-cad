"""Fix failing CadQuery scripts using Gemini (batch or single) or OpenAI.

Reads a TSV of failures (filename\terror), fixes each script using the
provided error context, and saves fixed versions.

Usage:
    # Gemini batch mode (recommended for large sets):
    python fix_cadquery.py --tsv failures.tsv --input_dir ./results --provider gemini --mode batch

    # Gemini single mode:
    python fix_cadquery.py --tsv failures.tsv --input_dir ./results --provider gemini --mode single --workers 4

    # OpenAI single mode:
    python fix_cadquery.py --tsv failures.tsv --input_dir ./results --provider openai --mode single
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SYSTEM_PROMPT = """You are an expert CadQuery developer. The following CadQuery Python code failed to execute with this error:

ERROR: {error}

Common mistakes to avoid:
- Do NOT use .hull(), .helix(), .filterByPosition(), .filterBy(), .filter_by(), .tangentArc(), .select(), .nearestToPoint(), .tube(), .fillet2D(), .workplaneFromShape(), .rotated() — these do NOT exist in CadQuery
- Do NOT call show_object() — this is CQ-editor only and will cause NameError
- polarArray() does not have an 'angleRange' parameter
- extrude() does not have a 'centered' parameter
- For fillets/chamfers, first select edges with .edges() before calling .fillet() or .chamfer()
- If you get "no solid on stack": build a solid first with box()/cylinder()/extrude() before doing cuts/fillets
- If you get "no pending wires": call rect()/circle()/polygon() before extrude()/revolve()

Fix the code so it runs without errors and produces valid solid geometry.
You may COMPLETELY REWRITE the code from scratch — do not try to patch the broken code.

Requirements:
- Use only standard CadQuery 2.x API methods
- Create a variable called 'result' containing the final geometry
- Include all necessary imports (import cadquery as cq)
- The code must be executable and create valid solid geometry

Return ONLY the Python code, no explanations, no markdown fences."""


def strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"): lines = lines[1:]
        if lines and lines[-1].strip() == "```": lines = lines[:-1]
        return "\n".join(lines)
    return text


def load_failures(tsv_path: Path):
    failures = []
    with open(tsv_path) as f:
        for line in f:
            parts = line.strip().split("\t", 1)
            if len(parts) == 2:
                failures.append((parts[0], parts[1]))
    return failures


def fix_gemini_single(client, code: str, error: str, model: str, thinking: str = None):
    from google.genai import types
    prompt = SYSTEM_PROMPT.format(error=error) + f"\n\nCODE:\n```python\n{code}\n```\n\nFixed code:"
    budget_map = {"LOW": 1024, "MEDIUM": 8000, "HIGH": -1}
    budget = budget_map.get((thinking or "").upper())
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=budget)
    ) if budget is not None else types.GenerateContentConfig()
    resp = client.models.generate_content(model=model, contents=prompt, config=config)
    return strip_fences(resp.text.strip())


def fix_openai_single(client, code: str, error: str, model: str):
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert CadQuery programmer."},
            {"role": "user", "content": SYSTEM_PROMPT.format(error=error) + f"\n\nCODE:\n```python\n{code}\n```\n\nFixed code:"}
        ],
        temperature=0.2,
    )
    return strip_fences(resp.choices[0].message.content.strip())


def run_batch_gemini(client, failures, input_dir: Path, output_dir: Path, model: str, chunk_name: str):
    """Submit a Gemini batch job to fix all failures at once."""
    from google.genai import types

    jsonl_path = Path(f"/tmp/{chunk_name}_fix_requests.jsonl")
    count = 0
    with open(jsonl_path, "w") as f:
        for name, error in failures:
            py_path = input_dir / name
            if not py_path.exists(): continue
            fix_path = output_dir / py_path.name.replace(".py", "_fix.py")
            if fix_path.exists(): continue
            code = py_path.read_text()
            prompt = SYSTEM_PROMPT.format(error=error) + f"\n\nCODE:\n```python\n{code}\n```\n\nFixed code:"
            entry = {
                "key": name,
                "request": {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"thinkingConfig": {"thinkingBudget": 8000}},
                }
            }
            f.write(json.dumps(entry) + "\n")
            count += 1

    if count == 0:
        print("No files to fix."); return

    print(f"Submitting batch with {count} requests...")
    uploaded = client.files.upload(file=str(jsonl_path),
                                   config=types.UploadFileConfig(display_name=chunk_name, mime_type="jsonl"))
    batch = client.batches.create(model=model, src=uploaded.name, config={"display_name": chunk_name})
    print(f"Batch job: {batch.name}")

    terminal = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}
    while batch.state.name not in terminal:
        print(f"  {batch.state.name} — waiting 60s...")
        time.sleep(60)
        batch = client.batches.get(name=batch.name)

    if batch.state.name != "JOB_STATE_SUCCEEDED":
        print(f"Batch failed: {batch.state.name}"); return

    content = client.files.download(file=batch.dest.file_name).decode("utf-8")
    saved = 0
    for line in content.splitlines():
        if not line.strip(): continue
        parsed = json.loads(line)
        key = parsed.get("key", "")
        try:
            parts = parsed["response"]["candidates"][0]["content"]["parts"]
            text = strip_fences("".join(p.get("text", "") for p in parts))
        except (KeyError, IndexError):
            continue
        fix_path = output_dir / Path(key).name.replace(".py", "_fix.py")
        fix_path.write_text(text)
        saved += 1
    print(f"Saved {saved} fixed files to {output_dir}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tsv",        required=True, help="TSV file: filename\\terror")
    parser.add_argument("--input_dir",  required=True, help="Directory with original .py files")
    parser.add_argument("--output_dir", default=None,  help="Where to save fixed files (default: same as input)")
    parser.add_argument("--provider",   choices=["gemini", "openai"], default="gemini")
    parser.add_argument("--mode",       choices=["batch", "single"], default="batch")
    parser.add_argument("--model",      default=None, help="Model (default: gemini-3.1-pro-preview / gpt-4o)")
    parser.add_argument("--thinking",   default=None, help="Gemini thinking level: LOW, MEDIUM, HIGH")
    parser.add_argument("--api_key",    default=None)
    parser.add_argument("--workers",    type=int, default=4)
    parser.add_argument("--max_fixes",  type=int, default=None)
    parser.add_argument("--chunk_name", default="fix_batch")
    args = parser.parse_args()

    input_dir  = Path(args.input_dir)
    output_dir = Path(args.output_dir) if args.output_dir else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    failures = load_failures(Path(args.tsv))
    if args.max_fixes:
        failures = failures[:args.max_fixes]
    print(f"Loaded {len(failures)} failures from {args.tsv}")

    if args.provider == "gemini":
        from google import genai
        key = args.api_key or os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=key)
        model = args.model or "gemini-3.1-pro-preview"

        if args.mode == "batch":
            run_batch_gemini(client, failures, input_dir, output_dir, model, args.chunk_name)
        else:
            def fix_one(item):
                name, error = item
                py_path = input_dir / name
                if not py_path.exists(): return name, False, "not found"
                fix_path = output_dir / name.replace(".py", "_fix.py")
                if fix_path.exists(): return name, True, "skipped"
                try:
                    fixed = fix_gemini_single(client, py_path.read_text(), error, model, args.thinking)
                    fix_path.write_text(fixed)
                    return name, True, "ok"
                except Exception as e:
                    return name, False, str(e)

            ok, failed = 0, 0
            with ThreadPoolExecutor(max_workers=args.workers) as exe:
                for name, success, msg in exe.map(fix_one, failures):
                    if success: ok += 1
                    else: failed += 1; print(f"  FAIL {name}: {msg}")
            print(f"Done: {ok} fixed, {failed} failed")

    elif args.provider == "openai":
        import openai
        key = args.api_key or os.environ.get("OPENAI_API_KEY")
        client = openai.OpenAI(api_key=key)
        model = args.model or "gpt-4o"

        def fix_one(item):
            name, error = item
            py_path = input_dir / name
            if not py_path.exists(): return name, False, "not found"
            fix_path = output_dir / name.replace(".py", "_fix.py")
            if fix_path.exists(): return name, True, "skipped"
            try:
                fixed = fix_openai_single(client, py_path.read_text(), error, model)
                fix_path.write_text(fixed)
                return name, True, "ok"
            except Exception as e:
                return name, False, str(e)

        ok, failed = 0, 0
        with ThreadPoolExecutor(max_workers=args.workers) as exe:
            for name, success, msg in exe.map(fix_one, failures):
                if success: ok += 1
                else: failed += 1; print(f"  FAIL {name}: {msg}")
        print(f"Done: {ok} fixed, {failed} failed")


if __name__ == "__main__":
    main()
