"""Generate CadQuery code from CAD images using Gemini.

Supports two modes:
  - batch:  Upload images to Gemini File API, submit a batch job, poll, download
  - single: Direct API calls (useful for testing small sets)

Use --multiview for images containing 4 views of the same object.

Usage:
    GEMINI_API_KEY=key python generate.py --input_dir ./images --output_dir ./results
    GEMINI_API_KEY=key python generate.py --input_dir ./images --output_dir ./results --multiview
    GEMINI_API_KEY=key python generate.py --input_dir ./images --output_dir ./results --mode single --max_images 10
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

PROMPT_SINGLE_VIEW = """You are an expert CAD engineer and 3D modeling specialist with deep knowledge of mechanical design, geometric modeling, and CadQuery.

Generate CadQuery Python code to create this 3D CAD model based on the provided image.

Requirements:
- Use CadQuery syntax
- Create a variable called 'result' containing the final geometry
- Include all necessary imports
- Use parametric dimensions where appropriate
- The code must be executable and create valid solid geometry

Return ONLY the Python code, no explanations."""

PROMPT_MULTI_VIEW = """You are an expert CAD engineer and 3D modeling specialist with deep knowledge of mechanical design, geometric modeling, and CadQuery.

The image shows a single 3D CAD model from 4 different viewpoints arranged in one image.

Generate CadQuery Python code to create this 3D CAD model based on the provided multi-view image.

Requirements:
- Use CadQuery syntax
- Create a variable called 'result' containing the final geometry
- Include all necessary imports
- Infer precise dimensions from the views, using floating-point values where needed (e.g. 12.5, 3.175, 25.4)
- Do NOT round dimensions to the nearest integer — match the proportions in the views as closely as possible
- The code must be executable and create valid solid geometry

Return ONLY the Python code, no explanations."""

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".heic"}


def get_mime(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


def collect_images(input_dir: Path, recursive: bool = False, exclude: set = None) -> list:
    glob = input_dir.rglob("*") if recursive else input_dir.iterdir()
    images = sorted(p for p in glob if p.suffix.lower() in SUPPORTED_EXTENSIONS)
    if exclude:
        images = [img for img in images if img not in exclude]
    if not images:
        raise FileNotFoundError(f"No images found in {input_dir}")
    return images


def out_path_for(img: Path, input_dir: Path, output_dir: Path, suffix: str) -> Path:
    rel = img.relative_to(input_dir)
    subdir = output_dir / rel.parent
    return subdir / f"{img.stem}{suffix}.py"


def strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"): lines = lines[1:]
        if lines and lines[-1].strip() == "```": lines = lines[:-1]
        return "\n".join(lines)
    return text


# ── Batch mode ──────────────────────────────────────────────────────────────

def upload_images(client, images: list, workers: int) -> dict:
    uploaded = {}
    done = 0
    def upload_one(img):
        f = client.files.upload(file=str(img),
                                config=types.UploadFileConfig(display_name=img.stem, mime_type=get_mime(img)))
        return img.name, f.uri
    with ThreadPoolExecutor(max_workers=workers) as exe:
        futures = {exe.submit(upload_one, img): img for img in images}
        for fut in as_completed(futures):
            name, uri = fut.result()
            uploaded[name] = uri
            done += 1
            if done % 50 == 0 or done == len(images):
                print(f"  Uploaded {done}/{len(images)}...")
    return uploaded


def build_jsonl(images: list, jsonl_path: Path, uploaded: dict, prompt: str,
                thinking_level: str, input_dir: Path):
    gen_config = {}
    if thinking_level:
        gen_config["thinkingConfig"] = {"thinkingLevel": thinking_level.upper()}
    with open(jsonl_path, "w") as f:
        for img in images:
            rel = img.relative_to(input_dir)
            key = "/".join(list(rel.parts[:-1]) + [img.stem]) if len(rel.parts) > 1 else img.stem
            req = {
                "key": key,
                "request": {
                    "contents": [{"parts": [
                        {"text": prompt},
                        {"file_data": {"file_uri": uploaded[img.name], "mime_type": get_mime(img)}}
                    ]}],
                    "generation_config": gen_config,
                }
            }
            f.write(json.dumps(req) + "\n")


def submit_batch(client, jsonl_path: Path, model: str) -> str:
    uploaded_jsonl = client.files.upload(file=str(jsonl_path),
                                         config=types.UploadFileConfig(display_name="cad-batch", mime_type="jsonl"))
    job = client.batches.create(model=model, src=uploaded_jsonl.name,
                                config={"display_name": "cad-generation-batch"})
    print(f"Created batch job: {job.name}")
    return job.name


def poll_until_done(client, job_name: str, interval: int):
    terminal = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}
    job = client.batches.get(name=job_name)
    while job.state.name not in terminal:
        print(f"  Status: {job.state.name} — waiting {interval}s...")
        time.sleep(interval)
        job = client.batches.get(name=job_name)
    print(f"Job finished: {job.state.name}")
    return job


def save_batch_results(client, job, output_dir: Path, input_dir: Path, suffix: str):
    if job.state.name != "JOB_STATE_SUCCEEDED":
        print(f"Job did not succeed: {job.state.name}"); return 0
    content = client.files.download(file=job.dest.file_name).decode("utf-8", errors="replace")
    count = 0
    for line in content.splitlines():
        if not line.strip(): continue
        parsed = json.loads(line)
        key = parsed.get("key", "")
        response = parsed.get("response", {})
        try:
            parts = response["candidates"][0]["content"]["parts"]
            code = strip_fences("".join(p.get("text", "") for p in parts))
        except (KeyError, IndexError):
            code = f"# Error: {json.dumps(response)}"
        key_path = Path(key)
        subdir = output_dir / key_path.parent
        subdir.mkdir(parents=True, exist_ok=True)
        (subdir / f"{key_path.name}{suffix}.py").write_text(code)
        count += 1
    return count


def run_batch(client, images, args, prompt):
    print(f"\n[1/5] Uploading {len(images)} images...")
    t0 = time.time()
    uploaded = upload_images(client, images, args.workers)
    print(f"  Done in {time.time()-t0:.0f}s")

    jsonl_path = Path("batch_requests.jsonl")
    print(f"\n[2/5] Building JSONL...")
    build_jsonl(images, jsonl_path, uploaded, prompt, args.thinking, Path(args.input_dir))

    print(f"\n[3/5] Submitting batch (model={args.model})...")
    job_name = submit_batch(client, jsonl_path, args.model)

    print(f"\n[4/5] Waiting for batch job...")
    job = poll_until_done(client, job_name, args.poll_interval)

    print(f"\n[5/5] Saving results...")
    n = save_batch_results(client, job, Path(args.output_dir), Path(args.input_dir), args.suffix)
    print(f"  Saved {n} files to {args.output_dir}")


# ── Single mode ──────────────────────────────────────────────────────────────

def run_single(client, images, args, prompt):
    import threading
    output_dir = Path(args.output_dir)
    semaphore = threading.Semaphore(args.workers)
    rpm_lock = threading.Lock()
    request_times = []

    def call_one(img):
        with semaphore:
            # rate limiting
            with rpm_lock:
                now = time.time()
                request_times[:] = [t for t in request_times if now - t < 60]
                if len(request_times) >= args.rpm:
                    time.sleep(60 - (now - request_times[0]) + 0.1)
                request_times.append(time.time())

            try:
                thinking_level = args.thinking.upper() if args.thinking and args.thinking.upper() != "OFF" else None
                gen_config = types.GenerateContentConfig()
                if thinking_level:
                    budget = {"LOW": 1024, "MEDIUM": 8000, "HIGH": -1}.get(thinking_level, 8000)
                    gen_config = types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(thinking_budget=budget))

                uploaded = client.files.upload(file=str(img),
                                               config=types.UploadFileConfig(display_name=img.stem, mime_type=get_mime(img)))
                resp = client.models.generate_content(
                    model=args.model,
                    contents=[prompt, {"file_data": {"file_uri": uploaded.uri, "mime_type": get_mime(img)}}],
                    config=gen_config
                )
                code = strip_fences(resp.text.strip())
                out = out_path_for(img, Path(args.input_dir), output_dir, args.suffix)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(code)
                return img.name, True, None
            except Exception as e:
                return img.name, False, str(e)

    ok = failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as exe:
        futures = {exe.submit(call_one, img): img for img in images}
        for i, fut in enumerate(as_completed(futures), 1):
            name, success, err = fut.result()
            if success: ok += 1
            else: failed += 1; print(f"  FAIL {name}: {err}")
            if i % 50 == 0 or i == len(images):
                print(f"  {i}/{len(images)}  ok={ok} failed={failed}")

    print(f"\nDone: {ok} ok, {failed} failed")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir",    required=True)
    parser.add_argument("--output_dir",   default="./results")
    parser.add_argument("--mode",         choices=["batch", "single"], default="batch")
    parser.add_argument("--multiview",    action="store_true", help="Use multi-view prompt (4 views per image)")
    parser.add_argument("--model",        default="gemini-3.1-pro-preview")
    parser.add_argument("--suffix",       default="_31")
    parser.add_argument("--thinking",     default=None, help="LOW, MEDIUM, HIGH")
    parser.add_argument("--poll_interval",type=int, default=30)
    parser.add_argument("--max_images",   type=int, default=None)
    parser.add_argument("--skip_existing",action="store_true")
    parser.add_argument("--skip",         type=int, default=0)
    parser.add_argument("--workers",      type=int, default=8)
    parser.add_argument("--rpm",          type=int, default=60, help="Max requests/min (single mode)")
    parser.add_argument("--recursive",    action="store_true")
    parser.add_argument("--api_key",      default=None)
    args = parser.parse_args()

    if args.suffix == "_31" and args.multiview:
        args.suffix = "_31_mv"

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY or pass --api_key")
    client = genai.Client(api_key=api_key)

    prompt = PROMPT_MULTI_VIEW if args.multiview else PROMPT_SINGLE_VIEW

    print(f"[1/6] Collecting images from {args.input_dir}...")
    images = collect_images(Path(args.input_dir), recursive=args.recursive)
    print(f"Found {len(images)} image(s)")

    if args.skip_existing:
        before = len(images)
        images = [img for img in images
                  if not out_path_for(img, Path(args.input_dir), Path(args.output_dir), args.suffix).exists()]
        print(f"  Skipped {before - len(images)} already done, {len(images)} remaining")
    if args.skip:
        images = images[args.skip:]
    if args.max_images:
        images = images[:args.max_images]

    if not images:
        print("Nothing to process."); return

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    if args.mode == "batch":
        run_batch(client, images, args, prompt)
    else:
        run_single(client, images, args, prompt)


if __name__ == "__main__":
    main()
