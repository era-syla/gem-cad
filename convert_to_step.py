"""Convert generated CadQuery Python files to STEP files.

Usage:
    python convert_to_step.py --input_dir ./gray_cad_1 --suffix _cq --workers 8
"""

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

_RUNNER = """
import sys
from pathlib import Path
from OCP.BRepCheck import BRepCheck_Analyzer
py_path = Path(sys.argv[1])
step_path = py_path.with_suffix('.step')
namespace = {}
exec(py_path.read_text(), namespace)
result = namespace.get('result') or namespace.get('solid') or namespace.get('shape') or namespace.get('part')
if result is None:
    print('ERROR: no result variable', file=sys.stderr)
    sys.exit(1)
if hasattr(result, 'val'):
    shape = result.val()
elif hasattr(result, 'exportStep'):
    shape = result
else:
    print(f'ERROR: not a CadQuery object ({type(result)})', file=sys.stderr)
    sys.exit(1)
analyzer = BRepCheck_Analyzer(shape.wrapped)
if not analyzer.IsValid():
    print('ERROR: BRepCheck validation failed', file=sys.stderr)
    sys.exit(1)
shape.exportStep(str(step_path))
"""


def convert_file(py_path: Path, timeout: int) -> tuple[str, bool, str]:
    try:
        proc = subprocess.run(
            [sys.executable, "-c", _RUNNER, str(py_path)],
            capture_output=True, text=True, timeout=timeout
        )
        if proc.returncode == 0:
            return py_path.name, True, ""
        error = proc.stderr.strip().split("\n")[-1] if proc.stderr else "non-zero exit"
        return py_path.name, False, error
    except subprocess.TimeoutExpired:
        return py_path.name, False, f"timeout after {timeout}s"
    except Exception as e:
        return py_path.name, False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Convert CadQuery .py files to STEP")
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--suffix", type=str, default="_cq",
                        help="Only convert files matching *{suffix}.py")
    parser.add_argument("--workers", type=int, default=8,
                        help="Parallel worker processes")
    parser.add_argument("--skip_existing", action="store_true",
                        help="Skip files that already have a .step file")
    parser.add_argument("--skip", type=int, default=0,
                        help="Skip the first N files (e.g. already processed in a previous run)")
    parser.add_argument("--samples", type=int, default=None,
                        help="Limit to first N files")
    parser.add_argument("--timeout", type=int, default=30,
                        help="Max seconds per file before killing it (default: 30)")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    fail_log = input_dir / "convert_failures.tsv"
    pattern = f"*{args.suffix}.py"
    py_files = sorted(input_dir.glob(pattern))

    if args.skip:
        py_files = py_files[args.skip:]
        print(f"  Skipped first {args.skip} files, {len(py_files)} remaining")

    if args.samples:
        py_files = py_files[:args.samples]

    if args.skip_existing:
        before = len(py_files)
        failed_names = set()
        if fail_log.exists():
            with open(fail_log) as f:
                for line in f:
                    failed_names.add(line.split("\t")[0].strip())
        py_files = [f for f in py_files if not f.with_suffix(".step").exists() and f.name not in failed_names]
        print(f"Skipped {before - len(py_files)} already done or previously failed")

    print(f"Converting {len(py_files)} files with {args.workers} workers...\n")

    ok, fail, done = 0, 0, 0
    log_lines = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(convert_file, f, args.timeout): f for f in py_files}
        for future in as_completed(futures):
            name, success, error = future.result()
            done += 1
            if success:
                ok += 1
            else:
                fail += 1
                log_lines.append(f"{name}\t{error}")
            if done % 500 == 0 or done == len(py_files):
                print(f"  [{done}/{len(py_files)}] {ok} ok, {fail} failed")
                if log_lines:
                    with open(fail_log, "a") as f:
                        f.write("\n".join(log_lines) + "\n")
                    log_lines = []
        print(f"\nFailures logged to {fail_log}")

    print(f"\nDone: {ok} converted, {fail} failed out of {len(py_files)}")


if __name__ == "__main__":
    main()
