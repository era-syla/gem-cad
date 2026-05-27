"""Fix failing CadQuery scripts using OpenAI or Gemini API.

Usage:
    python fix_cq_errors.py --input_dir ./gray_cad_1 --api_key YOUR_KEY
    python fix_cq_errors.py --input_dir ./gray_cad_1 --provider gemini --api_key YOUR_GEMINI_KEY
    python fix_cq_errors.py --input_dir ./gray_cad_1 --api_key YOUR_KEY --workers 4 --max_fixes 100
"""

import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SYSTEM_PROMPT = """You are an expert CadQuery programmer. You will be given a CadQuery Python script that failed with an error. Fix the script so it runs without errors and produces a valid 3D solid assigned to a variable called `result`.

Rules:
- Only output the fixed Python code, no explanation, no markdown fences
- Keep the same overall design intent
- The final result must be assigned to `result`
- Use only standard CadQuery (cadquery) API
"""

def fix_script_openai(client, py_path: Path, error: str, model: str) -> tuple[str, bool, str]:
    code = py_path.read_text()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Script:\n```python\n{code}\n```\n\nError:\n{error}\n\nFixed script:"}
            ],
            temperature=0.2,
        )
        fixed_code = response.choices[0].message.content.strip()
        return _save_fix(py_path, fixed_code)
    except Exception as e:
        return py_path.name, False, str(e)


def fix_script_gemini(client, py_path: Path, error: str, model: str, thinking: str = None) -> tuple[str, bool, str]:
    from google.genai import types
    code = py_path.read_text()
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nScript:\n```python\n{code}\n```\n\nError:\n{error}\n\nFixed script:"
        budget = {"LOW": 1024, "MEDIUM": 8000, "HIGH": -1}.get(thinking.upper(), 8000) if thinking else None
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=budget)
        ) if budget is not None else types.GenerateContentConfig()
        response = client.models.generate_content(model=model, contents=prompt, config=config)
        fixed_code = response.text.strip()
        return _save_fix(py_path, fixed_code)
    except Exception as e:
        return py_path.name, False, str(e)


def _save_fix(py_path: Path, fixed_code: str) -> tuple[str, bool, str]:
    if fixed_code.startswith("```"):
        lines = fixed_code.split("\n")
        fixed_code = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    fix_path = py_path.with_name(py_path.stem + "_fix.py")
    fix_path.write_text(fixed_code)
    return py_path.name, True, str(fix_path)


def main():
    parser = argparse.ArgumentParser(description="Fix failing CadQuery scripts with OpenAI or Gemini")
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--suffix", type=str, default="_cq", help="Suffix of the original files")
    parser.add_argument("--provider", type=str, default="openai", choices=["openai", "gemini"])
    parser.add_argument("--api_key", type=str, default=None)
    parser.add_argument("--model", type=str, default=None, help="Model to use (defaults: gpt-4o / gemini-3.1-pro-preview)")
    parser.add_argument("--thinking", type=str, default=None, help="Gemini thinking level: LOW, MEDIUM, HIGH")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max_fixes", type=int, default=None)
    args = parser.parse_args()

    if args.provider == "gemini":
        from google import genai
        api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise SystemExit("Provide --api_key or set GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        model = args.model or "gemini-3.1-pro-preview"
        fix_fn = fix_script_gemini
    else:
        from openai import OpenAI
        api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise SystemExit("Provide --api_key or set OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        model = args.model or "gpt-4o"
        fix_fn = fix_script_openai

    input_dir = Path(args.input_dir)
    fail_log = input_dir / "convert_failures.tsv"

    if not fail_log.exists():
        raise SystemExit(f"No failure log found at {fail_log}")

    to_fix = []
    with open(fail_log) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t", 1)
            name, error = parts[0], parts[1] if len(parts) > 1 else "unknown error"
            py_path = input_dir / name
            fix_path = py_path.with_name(py_path.stem + "_fix.py")
            if py_path.exists() and not fix_path.exists():
                to_fix.append((py_path, error))

    if args.max_fixes:
        to_fix = to_fix[:args.max_fixes]

    print(f"Fixing {len(to_fix)} scripts with {args.workers} workers (provider: {args.provider}, model: {model})...\n")

    ok, fail, done = 0, 0, 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fix_fn, client, py, err, model, args.thinking) if args.provider == "gemini" else executor.submit(fix_fn, client, py, err, model): py for py, err in to_fix}
        for future in as_completed(futures):
            name, success, info = future.result()
            done += 1
            if success:
                ok += 1
            else:
                fail += 1
                print(f"  FAIL: {name} — {info}")
            if done % 50 == 0 or done == len(to_fix):
                print(f"  [{done}/{len(to_fix)}] {ok} fixed, {fail} failed")

    print(f"\nDone: {ok} fixed, {fail} failed. Run convert_to_step.py with --suffix _cq_fix to convert them.")


if __name__ == "__main__":
    main()
