"""
Batch Gemini API caller for CAD model generation from images.

Usage:
    python batch_gemini.py --input_dir ./images --output_dir ./results

Requires:
    pip install google-genai
    export GEMINI_API_KEY=your_api_key
"""

import argparse
import base64
import json
import mimetypes
import os
import time
from pathlib import Path

from google import genai
from google.genai import types

# Prompt
GEMINI_PROMPT = """You are an expert CAD engineer and 
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

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".heic"}


def get_mime_type(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


def collect_images(input_dir: Path) -> list[Path]:
    images = sorted(
        p for p in input_dir.iterdir()
        if p.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    )
    if not images:
        raise FileNotFoundError(f"No images found in {input_dir}")
    print(f"Found {len(images)} image(s) in {input_dir}")
    return images


def build_jsonl(images: list[Path], jsonl_path: Path, uploaded_files: dict[str, str], thinking_level: str = None):
    """Build a JSONL file with one request per image."""
    generation_config = {}
    if thinking_level:
        generation_config["thinkingConfig"] = {"thinkingLevel": thinking_level.upper()}

    with open(jsonl_path, "w") as f:
        for img_path in images:
            request = {
                "key": img_path.stem,
                "request": {
                    "contents": [
                        {
                            "parts": [
                                {"text": GEMINI_PROMPT},
                                {
                                    "file_data": {
                                        "file_uri": uploaded_files[img_path.name],
                                        "mime_type": get_mime_type(img_path),
                                    }
                                },
                            ]
                        }
                    ],
                    "generation_config": generation_config,
                },
            }
            f.write(json.dumps(request) + "\n")
    print(f"Wrote {len(images)} requests to {jsonl_path}")


def upload_images(client: genai.Client, images: list[Path]) -> dict[str, str]:
    """Upload images via the File API and return {filename: file_uri} mapping."""
    uploaded = {}
    for img_path in images:
        print(f"  Uploading {img_path.name}...")
        uploaded_file = client.files.upload(
            file=str(img_path),
            config=types.UploadFileConfig(
                display_name=img_path.stem,
                mime_type=get_mime_type(img_path),
            ),
        )
        uploaded[img_path.name] = uploaded_file.uri
    print(f"Uploaded {len(uploaded)} image(s)")
    return uploaded


def submit_batch(client: genai.Client, jsonl_path: Path, model: str) -> str:
    """Upload the JSONL file and create a batch job. Returns the job name."""
    uploaded_jsonl = client.files.upload(
        file=str(jsonl_path),
        config=types.UploadFileConfig(
            display_name="cad-batch-requests",
            mime_type="jsonl",
        ),
    )
    print(f"Uploaded JSONL as: {uploaded_jsonl.name}")

    batch_job = client.batches.create(
        model=model,
        src=uploaded_jsonl.name,
        config={"display_name": "cad-generation-batch"},
    )
    print(f"Created batch job: {batch_job.name}")
    return batch_job.name


def poll_until_done(client: genai.Client, job_name: str, poll_interval: int = 30):
    """Poll the batch job until it reaches a terminal state."""
    terminal_states = {
        "JOB_STATE_SUCCEEDED",
        "JOB_STATE_FAILED",
        "JOB_STATE_CANCELLED",
        "JOB_STATE_EXPIRED",
    }

    batch_job = client.batches.get(name=job_name)
    while batch_job.state.name not in terminal_states:
        print(f"  Status: {batch_job.state.name} — waiting {poll_interval}s...")
        time.sleep(poll_interval)
        batch_job = client.batches.get(name=job_name)

    print(f"Job finished: {batch_job.state.name}")
    return batch_job


def save_results(client: genai.Client, batch_job, output_dir: Path, input_dir: Path, suffix: str = "_31"):
    """Download results and save each generated code to a .py file next to its source image."""
    if batch_job.state.name != "JOB_STATE_SUCCEEDED":
        print(f"Job did not succeed (state={batch_job.state.name}). No results to save.")
        return

    result_file_name = batch_job.dest.file_name
    content_bytes = client.files.download(file=result_file_name)
    content = content_bytes.decode("utf-8")

    count = 0
    for line in content.splitlines():
        if not line.strip():
            continue
        parsed = json.loads(line)
        key = parsed.get("key", f"unknown_{count}")
        response = parsed.get("response", {})

        # Extract text from response
        code = ""
        try:
            parts = response["candidates"][0]["content"]["parts"]
            code = "".join(p.get("text", "") for p in parts)
        except (KeyError, IndexError):
            code = f"# Error: could not parse response\n# Raw: {json.dumps(response)}"

        # Strip markdown fences if present
        if code.strip().startswith("```"):
            lines = code.strip().splitlines()
            # Remove first and last fence lines
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            code = "\n".join(lines)

        # Save next to the input image
        out_path = input_dir / f"{key}{suffix}.py"
        out_path.write_text(code)
        count += 1
        print(f"  Saved {out_path}")

    print(f"Saved {count} result(s) next to input images in {input_dir}")


def main():
    parser = argparse.ArgumentParser(description="Batch Gemini CAD code generation from images")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing input images")
    parser.add_argument("--output_dir", type=str, default="./results", help="Directory for output .py files")
    parser.add_argument("--model", type=str, default="gemini-3.1-pro-preview", help="Gemini model name")
    parser.add_argument("--suffix", type=str, default="_31", help="Suffix for output .py files")
    parser.add_argument("--thinking", type=str, default=None, help="Thinking level: LOW, MEDIUM, HIGH")
    parser.add_argument("--poll_interval", type=int, default=30, help="Seconds between status polls")
    parser.add_argument("--max_images", type=int, default=None, help="Limit number of images to process")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.is_dir():
        raise SystemExit(f"Input directory does not exist: {input_dir}")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set the GEMINI_API_KEY environment variable")

    client = genai.Client(api_key=api_key)

    t_start = time.time()

    # 1. Collect images
    print("\n[1/6] Collecting images...")
    images = collect_images(input_dir)
    if args.max_images:
        images = images[:args.max_images]
        print(f"  Limited to {len(images)} images")

    # 2. Upload images
    print("\n[2/6] Uploading images to Gemini File API...")
    t0 = time.time()
    uploaded_files = upload_images(client, images)
    t_upload = time.time() - t0
    print(f"  Upload took {t_upload:.0f}s ({t_upload/60:.1f}m)")

    # 3. Build JSONL
    jsonl_path = Path("batch_requests.jsonl")
    print(f"\n[3/6] Building JSONL request file ({jsonl_path})...")
    build_jsonl(images, jsonl_path, uploaded_files, thinking_level=args.thinking)

    # 4. Submit batch job
    print(f"\n[4/6] Submitting batch job (model={args.model})...")
    job_name = submit_batch(client, jsonl_path, args.model)

    # 5. Poll and save results
    print("\n[5/6] Waiting for batch job to complete...")
    t0 = time.time()
    batch_job = poll_until_done(client, job_name, args.poll_interval)
    t_batch = time.time() - t0
    save_results(client, batch_job, output_dir, input_dir, suffix=args.suffix)

    # 6. Summary
    t_total = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"TIMING")
    print(f"  Upload:     {t_upload:.0f}s ({t_upload/60:.1f}m)")
    print(f"  Batch job:  {t_batch:.0f}s ({t_batch/60:.1f}m)")
    print(f"  Total:      {t_total:.0f}s ({t_total/60:.1f}m)")

    if batch_job.state.name == "JOB_STATE_SUCCEEDED":
        content = client.files.download(file=batch_job.dest.file_name).decode("utf-8")
        tot_in, tot_out, tot_think, n_ok, n_err = 0, 0, 0, 0, 0
        for line in content.splitlines():
            if not line.strip():
                continue
            parsed = json.loads(line)
            if "error" in parsed:
                n_err += 1
                continue
            um = parsed.get("response", {}).get("usageMetadata", {})
            tot_in += um.get("promptTokenCount", 0)
            tot_out += um.get("candidatesTokenCount", 0)
            tot_think += um.get("thoughtsTokenCount", 0)
            n_ok += 1
        cost_in = tot_in / 1_000_000 * 1.00
        cost_out = (tot_out + tot_think) / 1_000_000 * 6.00
        print(f"\nRESULTS: {n_ok} succeeded, {n_err} errors")
        print(f"\nTOKENS")
        print(f"  Input:        {tot_in:>12,}")
        print(f"  Output:       {tot_out:>12,}")
        print(f"  Thinking:     {tot_think:>12,}")
        print(f"  Total:        {tot_in + tot_out + tot_think:>12,}")
        print(f"  Avg think/req:  {tot_think // max(n_ok, 1):,}")
        print(f"\nCOST (batch pricing: $1/M input, $6/M output+think)")
        print(f"  Input:      ${cost_in:.2f}")
        print(f"  Out+Think:  ${cost_out:.2f}")
        print(f"  Total:      ${cost_in + cost_out:.2f}")
        print(f"  Per sample: ${(cost_in + cost_out) / max(n_ok, 1):.4f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
