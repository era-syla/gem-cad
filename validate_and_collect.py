"""
Convert generated CadQuery files to STEP, validate with BRepCheck_Analyzer,
and collect valid pairs (py + step) into an output folder.

Each file is processed in an isolated subprocess to avoid OCC segfaults.

Usage:
    python validate_and_collect.py [--output_dir ./valid_cq] [--workers 8]
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

SEARCH_DIRS = ["new_batch", "images", "sketch_extrude_easy", "results"]
GENERATED_RE = re.compile(r"_step_\d+_\d+.*\.py$")
SKIP_RE = re.compile(r"(_dbg|_test)\.py$")

# Worker script run in subprocess for each file
WORKER = """
import sys, json
from pathlib import Path
from OCP.BRepCheck import BRepCheck_Analyzer

py_path = Path(sys.argv[1])
step_path = py_path.with_suffix(".step")
result_data = {"converted": False, "valid": False, "error": ""}

try:
    ns = {}
    exec(py_path.read_text(), ns)
    result = ns.get("result")
    if result is None:
        result_data["error"] = "no result variable"
    elif not hasattr(result, "val"):
        result_data["error"] = "result has no .val()"
    else:
        # Export to STEP if missing
        if not step_path.exists():
            result.val().exportStep(str(step_path))
            result_data["converted"] = True

        # Validate
        shape = result.val().wrapped
        analyzer = BRepCheck_Analyzer(shape)
        result_data["valid"] = bool(analyzer.IsValid())
except Exception as e:
    result_data["error"] = str(e)

print(json.dumps(result_data))
"""


def find_generated_py(base: Path, input_dir: Path = None) -> list:
    files = []
    if input_dir:
        dirs = [input_dir]
    else:
        dirs = [base / d for d in SEARCH_DIRS]
    for p in dirs:
        if not p.exists():
            continue
        for f in sorted(p.glob("*.py")):
            if SKIP_RE.search(f.name):
                continue
            if GENERATED_RE.search(f.name):
                files.append(f)
    return files


def process_file(py_path: Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, "-c", WORKER, str(py_path)],
            capture_output=True, text=True, timeout=60
        )
        if proc.stdout.strip():
            return json.loads(proc.stdout.strip().splitlines()[-1])
        return {"converted": False, "valid": False, "error": proc.stderr[-200:]}
    except subprocess.TimeoutExpired:
        return {"converted": False, "valid": False, "error": "timeout"}
    except Exception as e:
        return {"converted": False, "valid": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str, default="./valid_cq")
    parser.add_argument("--input_dir", type=str, default=None)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()

    base = Path(__file__).parent
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    input_dir = Path(args.input_dir) if args.input_dir else None

    files = find_generated_py(base, input_dir)
    n_already = sum(1 for f in files if f.with_suffix(".step").exists())
    print(f"Found {len(files)} generated .py files")
    print(f"  Already have .step: {n_already}")
    print(f"  Need conversion:    {len(files) - n_already}")
    print(f"  Workers:            {args.workers}\n")

    total = len(files)
    conv_ok = conv_fail = valid = invalid = 0
    lock = Lock()

    def handle(f):
        already_had_step = f.with_suffix(".step").exists()
        res = process_file(f)
        step = f.with_suffix(".step")
        if res["valid"] and step.exists():
            shutil.copy2(f, output_dir / f.name)
            shutil.copy2(step, output_dir / step.name)
        return already_had_step, res

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(handle, f): (i, f) for i, f in enumerate(files, 1)}
        done = 0
        for future in as_completed(futures):
            i, f = futures[future]
            already_had_step, res = future.result()
            done += 1
            with lock:
                if res["converted"]:
                    conv_ok += 1
                elif not already_had_step and not res["valid"]:
                    conv_fail += 1
                if res["valid"]:
                    valid += 1
                else:
                    invalid += 1
                    if res["error"]:
                        status = "FAIL" if not already_had_step and not res["converted"] else "INVALID"
                        print(f"  [{done}/{total}] {status}: {f.name} — {res['error'][:80]}")
                if done % 100 == 0:
                    print(f"  Progress: {done}/{total} | valid so far: {valid}")

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"  Total .py files:      {total}")
    print(f"  Newly converted:      {conv_ok}")
    print(f"  Failed to convert:    {conv_fail}")
    print(f"  Valid (BRepCheck):    {valid}")
    print(f"  Invalid/failed:       {invalid}")
    print(f"\nValid pairs saved to: {output_dir.resolve()}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
