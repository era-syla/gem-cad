"""Manage Gemini batch jobs: check status, poll until done, download results.

Usage:
    python manage_batches.py --check batches/abc123 --poll --output_dir ./results
    python manage_batches.py --check batches/abc123 batches/def456 --download --output_dir ./results
    python manage_batches.py --list
"""

import argparse
import json
import os
import time
from pathlib import Path

from google import genai

TERMINAL_STATES = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}


def get_client(api_key=None):
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("Set GEMINI_API_KEY or pass --api_key")
    return genai.Client(api_key=key)


def strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"): lines = lines[1:]
        if lines and lines[-1].strip() == "```": lines = lines[:-1]
        return "\n".join(lines)
    return text


def download_results(client, job, output_dir: Path, suffix: str, output_format: str):
    content = client.files.download(file=job.dest.file_name).decode("utf-8", errors="replace")
    output_dir.mkdir(parents=True, exist_ok=True)
    saved = 0
    for line in content.splitlines():
        if not line.strip(): continue
        parsed = json.loads(line)
        key = parsed.get("key", "")
        if not key: continue
        response = parsed.get("response", {})
        try:
            parts = response["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts)
        except (KeyError, IndexError):
            text = f"# Error: {json.dumps(response)}"

        text = strip_fences(text)
        key_path = Path(key)
        subdir = output_dir / key_path.parent
        subdir.mkdir(parents=True, exist_ok=True)

        if output_format == "jsonl":
            out = subdir / f"{key_path.name}{suffix}.jsonl"
            # try to parse as JSON for graph outputs
            try:
                obj = json.loads(text)
                out.write_text(json.dumps(obj))
            except json.JSONDecodeError:
                out.write_text(text)
        else:
            out = subdir / f"{key_path.name}{suffix}.py"
            out.write_text(text)
        saved += 1
    return saved


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check",      nargs="+", metavar="JOB_ID", help="Job ID(s) to check/download")
    parser.add_argument("--list",       action="store_true", help="List all batch jobs")
    parser.add_argument("--poll",       action="store_true", help="Poll until terminal state")
    parser.add_argument("--download",   action="store_true", help="Download results if succeeded")
    parser.add_argument("--output_dir", default="./results", help="Where to save downloaded files")
    parser.add_argument("--suffix",     default="_31", help="Suffix for saved files")
    parser.add_argument("--output_format", choices=["py", "jsonl"], default="py")
    parser.add_argument("--interval",   type=int, default=30, help="Poll interval in seconds")
    parser.add_argument("--api_key",    default=None)
    args = parser.parse_args()

    client = get_client(args.api_key)

    if args.list:
        jobs = list(client.batches.list())
        print(f"{'State':<30} {'Job ID':<50} {'Display Name'}")
        print("-" * 100)
        for job in jobs:
            print(f"{job.state.name:<30} {job.name:<50} {getattr(job, 'display_name', '')}")
        return

    if not args.check:
        parser.error("Provide --check JOB_ID or --list")

    output_dir = Path(args.output_dir)

    for job_id in args.check:
        job_name = job_id if job_id.startswith("batches/") else f"batches/{job_id}"
        job = client.batches.get(name=job_name)
        print(f"{job_name}: {job.state.name}")

        if args.poll and job.state.name not in TERMINAL_STATES:
            while job.state.name not in TERMINAL_STATES:
                print(f"  Status: {job.state.name} — waiting {args.interval}s...")
                time.sleep(args.interval)
                job = client.batches.get(name=job_name)
            print(f"  Finished: {job.state.name}")

        if (args.download or args.poll) and job.state.name == "JOB_STATE_SUCCEEDED":
            saved = download_results(client, job, output_dir, args.suffix, args.output_format)
            print(f"  Saved {saved} files to {output_dir}")
        elif job.state.name != "JOB_STATE_SUCCEEDED":
            print(f"  Skipping download (state={job.state.name})")


if __name__ == "__main__":
    main()
