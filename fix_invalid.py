"""
Fix invalid/failed CadQuery files by re-calling Claude with error context.

For each failed .py file:
  1. Find the corresponding source image
  2. Re-call Claude with the original error + a stricter prompt
  3. Save fixed code, re-validate with BRepCheck_Analyzer
  4. Report results

Usage:
    python fix_invalid.py [--suffix _fix] [--max N] [--model claude-sonnet-4-6] [--workers 8]
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

import anthropic

SEARCH_DIRS = ["new_batch", "images", "sketch_extrude_easy", "results"]
GENERATED_RE = re.compile(r"_step_\d+_\d+.*\.py$")
SKIP_RE = re.compile(r"(_dbg|_test|_fix)\.py$")

FIX_PROMPT = """You are an expert CadQuery engineer. The following CadQuery Python code failed with this error:

ERROR: {error}

Common mistakes to avoid:
- Do NOT use .hull(), .helix(), .filterByPosition(), .filterBy(), .filter_by(), .tangentArc(), .select(), .nearestToPoint(), .tube(), .fillet2D(), .workplaneFromShape(), .rotated() — these do NOT exist in CadQuery
- Do NOT call show_object() — this is CQ-editor only and will cause NameError
- Do NOT use .val() on Workplane to get .wrapped — use result.val().wrapped, not result.wrapped
- polarArray() does not have an 'angleRange' parameter
- extrude() does not have a 'centered' parameter
- spline() does not have 'close' or 'include_current' parameters
- polygon() requires both nSides and diameter arguments
- rotate() requires axisStartPoint, axisEndPoint, and angleDegrees arguments
- sweep() requires a path argument: sweep(path) — do NOT pass path as keyword arg
- loft() does NOT take a 'path' keyword argument — use loft([wire1, wire2]) only
- Do NOT use undefined variables like 'cutout', 'body', 'base' unless you define them first
- For fillets/chamfers, first select edges with .edges() before calling .fillet() or .chamfer()
- If you get "no solid on stack": build a solid first with box()/cylinder()/extrude() before doing cuts/fillets
- If you get "no pending wires": call rect()/circle()/polygon() before extrude()/revolve()

Generate CadQuery Python code for this 3D CAD model image.
You may COMPLETELY REWRITE the code from scratch — do not try to patch the broken code.
Produce whatever code is most likely to work, even if it looks nothing like the original.

Requirements:
- Use only standard CadQuery 2.x API methods
- Create a variable called 'result' containing the final geometry
- Include all necessary imports (import cadquery as cq)
- The code must be executable and create valid solid geometry

Return ONLY the Python code, no explanations, no markdown fences."""


def get_failed_files(base: Path, valid_dir: Path, input_dir: Path = None) -> list:
    """Return py files whose base stem has no entry in valid_cq (any suffix)."""
    valid_stems = set()
    for f in valid_dir.glob("**/*.py"):
        m = re.match(r"(.+_step_\d+_\d+)", f.stem)
        if m:
            valid_stems.add(m.group(1))

    failed = []
    dirs = [input_dir] if input_dir else [base / d for d in SEARCH_DIRS]
    for p in dirs:
        if not p.exists():
            continue
        for f in sorted(p.glob("*.py")):
            if SKIP_RE.search(f.name) or not GENERATED_RE.search(f.name):
                continue
            m = re.match(r"(.+_step_\d+_\d+)", f.stem)
            base_stem = m.group(1) if m else f.stem
            if base_stem not in valid_stems:
                failed.append(f)
    return failed


def run_validate(py_path: Path) -> dict:
    worker = """
import sys, json
from pathlib import Path
from OCP.BRepCheck import BRepCheck_Analyzer

py_path = Path(sys.argv[1])
r = {"valid": False, "error": ""}
try:
    ns = {}
    exec(py_path.read_text(), ns)
    result = ns.get("result")
    if result is None:
        r["error"] = "no result variable"
    elif not hasattr(result, "val"):
        r["error"] = "result has no .val()"
    else:
        shape = result.val().wrapped
        analyzer = BRepCheck_Analyzer(shape)
        r["valid"] = bool(analyzer.IsValid())
        if not r["valid"]:
            r["error"] = "BRepCheck failed"
except Exception as e:
    r["error"] = str(e)
print(json.dumps(r))
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", worker, str(py_path)],
            capture_output=True, text=True, timeout=60
        )
        if proc.stdout.strip():
            return json.loads(proc.stdout.strip().splitlines()[-1])
        return {"valid": False, "error": proc.stderr[-200:]}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def find_image(py_path: Path):
    """Find the source PNG for a generated py file."""
    m = re.match(r"(.+_step_\d+_\d+).*", py_path.stem)
    if not m:
        return None
    base_stem = m.group(1)
    img = py_path.parent / f"{base_stem}.png"
    if img.exists():
        return img
    for d in SEARCH_DIRS:
        img = Path(d) / f"{base_stem}.png"
        if img.exists():
            return img
    return None


def call_claude_fix(api_key: str, model: str, img_path: Path, error: str) -> str:
    img_bytes = img_path.read_bytes()
    b64 = base64.b64encode(img_bytes).decode()
    mime, _ = mimetypes.guess_type(str(img_path))
    mime = mime or "image/png"

    prompt = FIX_PROMPT.format(error=error[:300])
    client = anthropic.Anthropic(api_key=api_key)

    for attempt in range(5):
        try:
            message = client.messages.create(
                model=model,
                max_tokens=8192,
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}},
                ]}],
            )
            break
        except anthropic.BadRequestError:
            raise  # 400 errors won't succeed on retry
        except anthropic.APIConnectionError:
            if attempt < 4:
                time.sleep(10 * (attempt + 1))
            else:
                raise
        except anthropic.RateLimitError:
            if attempt < 4:
                time.sleep(30 * (attempt + 1))
            else:
                raise

    code = message.content[0].text

    # Strip markdown fences
    if code.strip().startswith("```"):
        lines = code.strip().splitlines()
        lines = lines[1:] if lines[0].startswith("```") else lines
        lines = lines[:-1] if lines and lines[-1].strip() == "```" else lines
        code = "\n".join(lines)
    return code


def process_one(args_tuple):
    i, total, py_path, api_key, model, suffix, output_dir = args_tuple

    img = find_image(py_path)
    if img is None:
        return i, "no_image", py_path.name, ""

    error_result = run_validate(py_path)
    error = error_result.get("error", "unknown error")

    try:
        code = call_claude_fix(api_key, model, img, error)
    except Exception as e:
        return i, "api_error", py_path.name, str(e)

    m = re.match(r"(.+_step_\d+_\d+).*", py_path.stem)
    base_stem = m.group(1) if m else py_path.stem
    fix_path = py_path.parent / f"{base_stem}{suffix}.py"
    fix_path.write_text(code)

    result = run_validate(fix_path)
    if result["valid"]:
        step_path = fix_path.with_suffix(".step")
        subprocess.run(
            [sys.executable, "-c", f"""
import sys
from pathlib import Path
ns = {{}}
exec(Path('{fix_path}').read_text(), ns)
r = ns.get('result')
if r and hasattr(r, 'val'):
    r.val().exportStep('{step_path}')
"""],
            capture_output=True, text=True, timeout=60
        )
        if step_path.exists():
            sample_dir = output_dir / fix_path.stem
            sample_dir.mkdir(exist_ok=True)
            shutil.copy2(fix_path, sample_dir / fix_path.name)
            shutil.copy2(step_path, sample_dir / step_path.name)
            return i, "fixed", py_path.name, error
        else:
            return i, "step_fail", py_path.name, error
    else:
        return i, "still_fail", py_path.name, result["error"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="claude-sonnet-4-6")
    parser.add_argument("--suffix", type=str, default="_fix")
    parser.add_argument("--max", type=int, default=None)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output_dir", type=str, default="./valid_cq")
    parser.add_argument("--input_dir", type=str, default=None)
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("Set ANTHROPIC_API_KEY")

    base = Path(__file__).parent
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    input_dir = Path(args.input_dir) if args.input_dir else None

    print("Scanning for failed files...")
    failed = get_failed_files(base, output_dir, input_dir)
    print(f"Found {len(failed)} failed/invalid files\n")

    if args.max:
        failed = failed[:args.max]
        print(f"Limited to {args.max} files\n")

    total = len(failed)
    fixed = no_image = still_fail = 0
    print_lock = Lock()

    tasks = [
        (i, total, py_path, api_key, args.model, args.suffix, output_dir)
        for i, py_path in enumerate(failed, 1)
    ]

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_one, t): t for t in tasks}
        for future in as_completed(futures):
            i, status, name, detail = future.result()
            with print_lock:
                if status == "fixed":
                    fixed += 1
                    print(f"[{i}/{total}] FIXED ✓  {name}  ({detail[:50]})")
                elif status == "no_image":
                    no_image += 1
                    print(f"[{i}/{total}] NO IMAGE: {name}")
                else:
                    still_fail += 1
                    label = {"api_error": "API ERR", "step_fail": "STEP FAIL", "still_fail": "FAIL"}.get(status, status)
                    print(f"[{i}/{total}] {label}: {name}  — {detail[:120]}")

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"  Attempted:    {total}")
    print(f"  Fixed:        {fixed}")
    print(f"  No image:     {no_image}")
    print(f"  Still failed: {still_fail}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
