#!/usr/bin/env python3
"""
Batch image-to-CadQuery script using Google AI Batch API (inline requests).
Uploads images to Gemini File API, submits batch job, saves .py outputs.

Usage:
    python batch_images.py \
        --input_dir /path/to/images \
        --output_dir /path/to/output \
        --api_key AIza...
"""

import argparse
import json
import mimetypes
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from google import genai
from google.genai import types

# ── Config ───────────────────────────────────────────────────────────────────
MODEL              = "gemini-3.1-pro-preview"
CHUNK_SIZE         = 1000
POLL_INTERVAL      = 30
THINKING_LEVEL     = "MEDIUM"
SUPPORTED_EXTS     = {".png", ".jpg", ".jpeg", ".webp", ".heic"}

PROMPT = """You are an expert CAD engineer and
3D modeling specialist with deep knowledge of
mechanical design, geometric modeling, and CadQuery.

Generate CadQuery Python code to create this 3D CAD model
based on the provided image.

Requirements:
- Use CadQuery syntax
- Create a variable called 'result' containing the final geometry
- Include all necessary imports
- Use parametric dimensions where appropriate
- The code must be executable and create valid solid geometry

Return ONLY the Python code, no explanations."""

# ── Helpers ──────────────────────────────────────────────────────────────────

def get_mime_type(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "image/png"


def collect_images(input_dir: Path, recursive: bool = False) -> list[Path]:
    if recursive:
        images = sorted(p for p in input_dir.rglob("*") if p.suffix.lower() in SUPPORTED_EXTS)
    else:
        images = sorted(p for p in input_dir.iterdir() if p.suffix.lower() in SUPPORTED_EXTS)
    print(f"Found {len(images)} image(s)")
    return images


def upload_images(client, images: list[Path], workers: int = 8) -> dict[str, str]:
    """Upload images via File API. Returns {filename: file_uri}."""
    uploaded = {}

    def upload_one(img):
        f = client.files.upload(
            file=str(img),
            config=types.UploadFileConfig(display_name=img.stem, mime_type=get_mime_type(img)),
        )
        return img.name, f.uri

    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(upload_one, img): img for img in images}
        for future in as_completed(futures):
            name, uri = future.result()
            uploaded[name] = uri
            done += 1
            if done % 100 == 0 or done == len(images):
                print(f"  Uploaded {done}/{len(images)}...")

    return uploaded


def build_request(key: str, file_uri: str, mime_type: str) -> dict:
    return {
        "key": key,
        "request": {
            "contents": [{
                "role": "user",
                "parts": [
                    {"text": PROMPT},
                    {"file_data": {"file_uri": file_uri, "mime_type": mime_type}},
                ],
            }],
            "generation_config": {
                "thinkingConfig": {"thinkingLevel": THINKING_LEVEL},
            },
        },
    }


def submit_and_poll(client, jsonl_path: Path, model: str) -> object:
    uploaded_jsonl = client.files.upload(
        file=str(jsonl_path),
        config=types.UploadFileConfig(display_name="cad-batch-requests", mime_type="jsonl"),
    )
    batch = client.batches.create(
        model=model,
        src=uploaded_jsonl.name,
        config={"display_name": "cad-image-batch"},
    )
    print(f"  Job: {batch.name}")

    terminal = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}
    while batch.state.name not in terminal:
        print(f"  Status: {batch.state.name} — waiting {POLL_INTERVAL}s...")
        time.sleep(POLL_INTERVAL)
        batch = client.batches.get(name=batch.name)

    print(f"  Job finished: {batch.state.name}")
    return batch


def save_results(client, batch, output_dir: Path, suffix: str, input_dir: Path):
    if batch.state.name != "JOB_STATE_SUCCEEDED":
        print(f"Job did not succeed: {batch.state.name}")
        return

    content = client.files.download(file=batch.dest.file_name).decode("utf-8")
    count, errors = 0, 0

    for line in content.splitlines():
        if not line.strip():
            continue
        parsed = json.loads(line)
        key = parsed.get("key", f"unknown_{count}")
        response = parsed.get("response", {})

        try:
            parts = response["candidates"][0]["content"]["parts"]
            code = "".join(p.get("text", "") for p in parts)
        except (KeyError, IndexError):
            code = f"# Error: could not parse response\n# {json.dumps(response)}"
            errors += 1

        # Strip markdown fences
        if code.strip().startswith("```"):
            lines = code.strip().splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            code = "\n".join(lines)

        # Mirror subfolder structure
        key_path = Path(key)
        subdir = output_dir / key_path.parent
        subdir.mkdir(parents=True, exist_ok=True)
        out = subdir / f"{key_path.name}{suffix}.py"
        out.write_text(code)
        count += 1

    print(f"Saved {count} files to {output_dir} ({errors} errors)")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Batch image-to-CadQuery via Google AI")
    parser.add_argument("--input_dir",  required=True,  type=Path)
    parser.add_argument("--output_dir", required=True,  type=Path)
    parser.add_argument("--suffix",     default="_31",  help="Suffix for output .py files")
    parser.add_argument("--model",      default=MODEL)
    parser.add_argument("--skip_existing", action="store_true")
    parser.add_argument("--recursive",  action="store_true")
    parser.add_argument("--max_images", type=int, default=None)
    parser.add_argument("--workers",    type=int, default=8)
    parser.add_argument("--api_key",    type=str, default=None)
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY or pass --api_key")

    client = genai.Client(api_key=api_key)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Collect images
    print("\n[1/5] Collecting images...")
    images = collect_images(args.input_dir, recursive=args.recursive)

    if args.skip_existing:
        before = len(images)
        def _out(img):
            rel = img.relative_to(args.input_dir)
            return args.output_dir / rel.parent / f"{img.stem}{args.suffix}.py"
        images = [img for img in images if not _out(img).exists()]
        print(f"  Skipped {before - len(images)} already done, {len(images)} remaining")

    if args.max_images:
        images = images[:args.max_images]
        print(f"  Limited to {len(images)} images")

    if not images:
        print("Nothing to do.")
        return

    # 2. Upload images
    print("\n[2/5] Uploading images...")
    t0 = time.time()
    uploaded = upload_images(client, images, workers=args.workers)
    print(f"  Upload took {time.time()-t0:.0f}s")

    # 3. Build JSONL (chunked)
    chunks = [images[i:i+CHUNK_SIZE] for i in range(0, len(images), CHUNK_SIZE)]
    print(f"\n[3/5] Submitting {len(chunks)} batch job(s) of ≤{CHUNK_SIZE}...")

    t_start = time.time()
    for idx, chunk in enumerate(chunks, 1):
        jsonl_path = Path(f"batch_requests_chunk{idx}.jsonl")
        with open(jsonl_path, "w") as f:
            for img in chunk:
                rel = img.relative_to(args.input_dir)
                key = "/".join(list(rel.parts[:-1]) + [img.stem]) if len(rel.parts) > 1 else img.stem
                f.write(json.dumps(build_request(key, uploaded[img.name], get_mime_type(img))) + "\n")

        # 4. Submit & poll
        print(f"\n[4/5] Chunk {idx}/{len(chunks)} — submitting...")
        batch = submit_and_poll(client, jsonl_path, args.model)

        # 5. Save results
        print(f"\n[5/5] Chunk {idx}/{len(chunks)} — saving results...")
        save_results(client, batch, args.output_dir, args.suffix, args.input_dir)

    print(f"\nTotal time: {(time.time()-t_start)/60:.1f}m")


if __name__ == "__main__":
    main()
