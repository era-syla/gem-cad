"""Single (non-batch) Gemini API calls for quick testing.

Usage:
    python single_gemini.py --input_dir ./images --max_images 10 --model gemini-3.1-pro-preview --suffix _31
    python single_gemini.py --input_dir ./images --max_images 10 --suffix _31_low --thinking LOW
"""

import argparse
import base64
import json
import mimetypes
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

import requests

GEMINI_PROMPT = """You are an expert CAD engineer and 3D modeling specialist with deep knowledge of \
mechanical design, geometric modeling, and CadQuery.

Generate CadQuery Python code to create this 3D CAD model based on the provided image.

Requirements:
- Use CadQuery syntax
- Create a variable called 'result' containing the final geometry
- Include all necessary imports
- Use parametric dimensions where appropriate
- The code must be executable and create valid solid geometry

Return ONLY the Python code, no explanations."""

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".heic"}

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def get_mime_type(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


def call_gemini(api_key, model, img_path, thinking_level=None, thinking_budget=None, debug=False):
    """Call Gemini API directly via REST to support thinking_level and thinkingBudget."""
    img_bytes = img_path.read_bytes()
    b64_data = base64.b64encode(img_bytes).decode("utf-8")
    mime = get_mime_type(img_path)

    body = {
        "contents": [
            {
                "parts": [
                    {"text": GEMINI_PROMPT},
                    {"inline_data": {"mime_type": mime, "data": b64_data}},
                ]
            }
        ],
    }

    if thinking_level or thinking_budget:
        thinking_config = {}
        if thinking_level:
            thinking_config["thinkingLevel"] = thinking_level.upper()
        if thinking_budget:
            thinking_config["thinkingBudget"] = thinking_budget
        body["generationConfig"] = {"thinkingConfig": thinking_config}

    url = API_URL.format(model=model) + f"?key={api_key}"
    for attempt in range(3):
        try:
            resp = requests.post(url, json=body, timeout=600)
            break
        except requests.exceptions.ReadTimeout:
            if attempt < 2:
                print(f"\ntimeout, retrying ({attempt+2}/3)...", end=" ", flush=True)
                time.sleep(5)
            else:
                raise
    if resp.status_code != 200:
        print(f"\nAPI error {resp.status_code}: {resp.text[:500]}")
    resp.raise_for_status()
    data = resp.json()

    if debug:
        print(f"\n--- RAW usageMetadata ---")
        print(json.dumps(data.get("usageMetadata", {}), indent=2))
        # Also show part types (thought vs text)
        for ci, candidate in enumerate(data.get("candidates", [])):
            for pi, part in enumerate(candidate.get("content", {}).get("parts", [])):
                part_keys = list(part.keys())
                preview = ""
                if "text" in part:
                    preview = part["text"][:80] + "..."
                elif "thought" in part:
                    preview = str(part["thought"])[:80] + "..."
                print(f"  candidate[{ci}].parts[{pi}]: keys={part_keys}  {preview}")
        print("---\n")

    # Extract text
    text = ""
    for candidate in data.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "text" in part:
                text += part["text"]

    # Extract usage
    usage = data.get("usageMetadata", {})
    inp = usage.get("promptTokenCount", 0)
    out = usage.get("candidatesTokenCount", 0)
    think = usage.get("thoughtsTokenCount", 0)

    return text, inp, out, think


def main():
    parser = argparse.ArgumentParser(description="Single Gemini API calls for testing")
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--model", type=str, default="gemini-3.1-pro-preview")
    parser.add_argument("--max_images", type=int, default=None)
    parser.add_argument("--suffix", type=str, default="_31", help="Suffix for output files")
    parser.add_argument("--skip", type=int, default=0, help="Skip first N images")
    parser.add_argument("--thinking", type=str, default=None,
                        help="Thinking level: LOW, MEDIUM, HIGH, or OFF")
    parser.add_argument("--thinking_budget", type=int, default=None,
                        help="Max thinking tokens (e.g. 1024, 2048)")
    parser.add_argument("--files", type=str, default=None,
                        help="Comma-separated list of specific image filenames to process")
    parser.add_argument("--debug", action="store_true",
                        help="Print raw API response metadata")
    parser.add_argument("--workers", type=int, default=1, help="Parallel workers")
    parser.add_argument("--rpm", type=int, default=60, help="Max requests per minute")
    parser.add_argument("--prefix", type=str, default="", help="Prefix for output filenames")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set the GEMINI_API_KEY environment variable")

    if args.files:
        images = [input_dir / f.strip() for f in args.files.split(",")]
        images = [p for p in images if p.exists()]
    else:
        all_images = sorted(
            p for p in input_dir.iterdir()
            if p.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
        )
        images = all_images[args.skip:args.skip + args.max_images] if args.max_images else all_images[args.skip:]

    print(f"Processing {len(images)} images with {args.model}...")
    if args.thinking:
        print(f"Thinking level: {args.thinking.upper()}")
    if args.thinking_budget:
        print(f"Thinking budget: {args.thinking_budget} tokens")
    print()

    tot_in, tot_out, tot_think = 0, 0, 0
    t_start = time.time()
    print_lock = Lock()
    rate_lock = Lock()
    last_req_time = [0.0]
    min_interval = 60.0 / args.rpm  # seconds between requests

    def process_one(idx_img):
        i, img_path = idx_img
        out_path = input_dir / f"{args.prefix}{img_path.stem}{args.suffix}.py"
        if out_path.exists():
            with print_lock:
                print(f"[{i}/{len(images)}] {img_path.name}... skipped (exists)")
            return 0, 0, 0

        # Rate limit
        with rate_lock:
            now = time.time()
            wait = min_interval - (now - last_req_time[0])
            if wait > 0:
                time.sleep(wait)
            last_req_time[0] = time.time()

        with print_lock:
            print(f"[{i}/{len(images)}] {img_path.name}...", end=" ", flush=True)
        t0 = time.time()

        code, inp, out, think = call_gemini(
            api_key, args.model, img_path, thinking_level=args.thinking,
            thinking_budget=args.thinking_budget, debug=args.debug
        )

        # Strip markdown fences
        if code.strip().startswith("```"):
            lines = code.strip().splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            code = "\n".join(lines)

        out_path.write_text(code)
        elapsed = time.time() - t0
        with print_lock:
            print(f"done in {elapsed:.1f}s (out={out}, think={think})")
        return inp, out, think

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(process_one, (i+1, img)) for i, img in enumerate(images)]
        for future in as_completed(futures):
            inp, out, think = future.result()
            tot_in += inp
            tot_out += out
            tot_think += think

    t_total = time.time() - t_start
    n = max(len(images), 1)
    cost_in = tot_in / 1_000_000 * 2.50
    cost_out = (tot_out + tot_think) / 1_000_000 * 15.00

    print(f"\n{'='*60}")
    print(f"Model: {args.model}")
    if args.thinking:
        print(f"Thinking: {args.thinking.upper()}")
    if args.thinking_budget:
        print(f"Thinking budget: {args.thinking_budget}")
    print(f"Total time: {t_total:.0f}s ({t_total/60:.1f}m)")
    print(f"\nTOKENS")
    print(f"  Input:        {tot_in:>10,}")
    print(f"  Output:       {tot_out:>10,}")
    print(f"  Thinking:     {tot_think:>10,}")
    print(f"  Total:        {tot_in + tot_out + tot_think:>10,}")
    print(f"  Avg think/req:  {tot_think // max(n, 1):,}")
    print(f"\nCOST (standard pricing: $2.50/M input, $15/M output+think)")
    print(f"  Input:      ${cost_in:.2f}")
    print(f"  Out+Think:  ${cost_out:.2f}")
    print(f"  Total:      ${cost_in + cost_out:.2f}")
    print(f"  Per sample: ${(cost_in + cost_out) / max(n, 1):.4f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
