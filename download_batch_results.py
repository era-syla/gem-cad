"""
Download results from completed Gemini batch jobs.

Usage:
    GEMINI_API_KEY=your_key python download_batch_results.py \
        --jobs JOB_ID1 JOB_ID2 ... \
        --output_dir /Users/erasyla/abc-rendering/gray_cad_1 \
        --suffix _cq
"""

import argparse
import json
import os
from pathlib import Path

from google import genai


def save_job_results(client, batch_job, output_dir: Path, suffix: str):
    job_id = batch_job.name.split("/")[-1]
    state = batch_job.state.name
    print(f"\n[{job_id}] State: {state}")

    if state != "JOB_STATE_SUCCEEDED":
        print(f"[{job_id}] Skipping (not SUCCEEDED)")
        return 0

    result_file_name = batch_job.dest.file_name
    print(f"[{job_id}] Downloading results from {result_file_name}...")
    content_bytes = client.files.download(file=result_file_name)
    content = content_bytes.decode("utf-8")

    count = 0
    errors = 0
    for line in content.splitlines():
        if not line.strip():
            continue
        parsed = json.loads(line)
        key = parsed.get("key", f"unknown_{count}")

        if "error" in parsed:
            errors += 1
            continue

        response = parsed.get("response", {})
        code = ""
        try:
            parts = response["candidates"][0]["content"]["parts"]
            code = "".join(p.get("text", "") for p in parts)
        except (KeyError, IndexError):
            code = f"# Error: could not parse response\n# Raw: {json.dumps(response)}"

        # Strip markdown fences
        if code.strip().startswith("```"):
            lines = code.strip().splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            code = "\n".join(lines)

        out_path = output_dir / f"{key}{suffix}.py"
        if out_path.exists():
            continue  # already downloaded
        out_path.write_text(code)
        count += 1

    print(f"[{job_id}] Saved {count} new files ({errors} errors) to {output_dir}")
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", nargs="+", required=True, help="Job IDs to download (short IDs)")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save .py files")
    parser.add_argument("--suffix", type=str, default="_cq", help="Suffix for output .py files")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY environment variable")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = genai.Client(api_key=api_key)

    # Normalize requested IDs to short form
    wanted = {j.split("/")[-1] for j in args.jobs}
    print(f"Looking for {len(wanted)} job(s) via batches.list()...")

    found = {}
    for job in client.batches.list():
        short_id = job.name.split("/")[-1]
        if short_id in wanted:
            found[short_id] = job
            print(f"  Found: {short_id} ({job.state.name})")

    not_found = wanted - set(found.keys())
    if not_found:
        print(f"\nWARNING: {len(not_found)} job(s) not found in your account: {not_found}")

    total = 0
    for short_id, batch_job in found.items():
        total += save_job_results(client, batch_job, output_dir, args.suffix)

    print(f"\nDone. Total files saved: {total}")


if __name__ == "__main__":
    main()
