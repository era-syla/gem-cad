"""
Check status of a submitted Gemini batch job and download results if complete.

Usage:
    python check_batch_status.py --batch batches/w308fxmja1xd3dgjcivbfb2464iq9fgxag22 \
        --apikey AIza... --out graphs.jsonl
"""

import argparse
import json
import re
import sys
import time

from google import genai


def parse_graph(text: str):
    text = text.strip()
    m = re.match(r"^```(?:python|json)?\s*(.*?)```\s*$", text, re.DOTALL)
    text = m.group(1).strip() if m else text
    try:
        obj = json.loads(text)
        if isinstance(obj, list):
            return obj
    except json.JSONDecodeError:
        pass
    m = re.search(r"\[.*\]", text, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group())
            if isinstance(obj, list):
                return obj
        except json.JSONDecodeError:
            pass
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch",  required=True, help="e.g. batches/w308fxmja1xd3dgjcivbfb2464iq9fgxag22")
    parser.add_argument("--apikey", required=True)
    parser.add_argument("--out",    default=None, help="JSONL file to append results to (optional)")
    parser.add_argument("--poll",   action="store_true", help="Keep polling until terminal state")
    parser.add_argument("--interval", type=int, default=30)
    args = parser.parse_args()

    client = genai.Client(api_key=args.apikey)

    terminal = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}

    batch = client.batches.get(name=args.batch)
    print(f"Job: {batch.name}")
    print(f"State: {batch.state.name}")

    if args.poll and batch.state.name not in terminal:
        print("Polling...", flush=True)
        while batch.state.name not in terminal:
            print(f"  state={batch.state.name}", flush=True)
            time.sleep(args.interval)
            batch = client.batches.get(name=args.batch)
        print(f"Finished: {batch.state.name}")

    if batch.state.name != "JOB_STATE_SUCCEEDED":
        print(f"Job did not succeed — nothing to download.")
        sys.exit(1)

    print("Downloading results...")
    content = client.files.download(file=batch.dest.file_name).decode("utf-8")
    lines = [l for l in content.splitlines() if l.strip()]
    print(f"  {len(lines)} result lines")

    if not args.out:
        print("No --out specified, skipping save.")
        return

    saved = 0
    skipped = 0
    with open(args.out, "a") as f:
        for line in lines:
            parsed = json.loads(line)
            key = parsed.get("key", "")
            if not key:
                continue
            try:
                parts = parsed["response"]["candidates"][0]["content"]["parts"]
                text = "".join(p.get("text", "") for p in parts)
            except (KeyError, IndexError):
                skipped += 1
                continue
            graph = parse_graph(text)
            if graph:
                f.write(json.dumps({"source": key, "graph": graph}) + "\n")
                saved += 1
            else:
                print(f"  SKIP [{key}]: could not parse graph JSON")
                skipped += 1

    print(f"Saved {saved} graphs to {args.out} ({skipped} skipped)")


if __name__ == "__main__":
    main()
