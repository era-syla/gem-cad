"""Fix failing CadQuery scripts via Gemini Batch API.

Usage:
    python batch_fix_chunks.py --tsv /tmp/fix_chunk4.tsv --api_key AIza... --chunk_name chunk4
"""

import argparse
import json
import time
from pathlib import Path

from google import genai
from google.genai import types

SYSTEM_PROMPT = """You are an expert CadQuery programmer. You will be given a CadQuery Python script that failed with an error. Fix the script so it runs without errors and produces a valid 3D solid assigned to a variable called `result`.

Rules:
- Only output the fixed Python code, no explanation, no markdown fences
- Keep the same overall design intent
- The final result must be assigned to `result`
- Use only standard CadQuery (cadquery) API
"""

def build_jsonl(tsv_path: Path, py_dir: Path, jsonl_path: Path) -> int:
    count = 0
    with open(tsv_path) as f_in, open(jsonl_path, "w") as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t", 1)
            name, error = parts[0], parts[1] if len(parts) > 1 else "unknown error"
            py_path = py_dir / name
            if not py_path.exists():
                continue
            fix_path = py_path.with_name(py_path.stem + "_fix.py")
            if fix_path.exists():
                continue
            code = py_path.read_text()
            prompt = f"{SYSTEM_PROMPT}\n\nScript:\n```python\n{code}\n```\n\nError:\n{error}\n\nFixed script:"
            entry = {
                "key": name,
                "request": {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"thinkingConfig": {"thinkingBudget": 8000}},
                }
            }
            f_out.write(json.dumps(entry) + "\n")
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tsv", required=True)
    parser.add_argument("--api_key", required=True)
    parser.add_argument("--chunk_name", default="chunk")
    parser.add_argument("--py_dir", default="/Users/erasyla/gem-cad/all_31_py")
    parser.add_argument("--model", default="gemini-3.1-pro-preview")
    parser.add_argument("--poll_interval", type=int, default=60)
    args = parser.parse_args()

    client = genai.Client(api_key=args.api_key)
    tsv_path = Path(args.tsv)
    py_dir = Path(args.py_dir)

    print(f"Loaded failures from {tsv_path}")

    jsonl_path = Path(f"/tmp/{args.chunk_name}_requests.jsonl")
    count = build_jsonl(tsv_path, py_dir, jsonl_path)
    print(f"Samples to fix: {count}")
    if count == 0:
        print("Nothing to fix.")
        return

    # Upload JSONL
    uploaded = client.files.upload(
        file=str(jsonl_path),
        config=types.UploadFileConfig(display_name=f"{args.chunk_name}-fix", mime_type="jsonl"),
    )
    print(f"  [{args.chunk_name}] uploaded JSONL: {uploaded.name}")

    # Submit batch job
    batch_job = client.batches.create(
        model=args.model,
        src=uploaded.name,
        config={"display_name": f"fix-{args.chunk_name}"},
    )
    print(f"  [{args.chunk_name}] job={batch_job.name}")

    # Poll
    terminal = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}
    while batch_job.state.name not in terminal:
        print(f"  [{args.chunk_name}] state={batch_job.state.name}")
        time.sleep(args.poll_interval)
        batch_job = client.batches.get(name=batch_job.name)
    print(f"  [{args.chunk_name}] finished: {batch_job.state.name}")

    if batch_job.state.name != "JOB_STATE_SUCCEEDED":
        print("Job did not succeed.")
        return

    # Download and save results
    content = client.files.download(file=batch_job.dest.file_name).decode("utf-8")
    saved = 0
    for line in content.splitlines():
        if not line.strip():
            continue
        parsed = json.loads(line)
        key = parsed.get("key", "")
        if not key:
            continue
        try:
            parts = parsed["response"]["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts)
        except (KeyError, IndexError):
            continue
        text = text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        py_path = py_dir / key
        fix_path = py_path.with_name(py_path.stem + "_fix.py")
        fix_path.write_text(text)
        saved += 1

    print(f"\nChunk {args.chunk_name} — {saved} files fixed so far")
    print(f"\nDone. {saved} fixed files saved.")


if __name__ == "__main__":
    main()
