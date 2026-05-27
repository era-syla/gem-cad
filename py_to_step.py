"""Convert CadQuery Python files to STEP, with optional geometry validation.

Input can be a directory of .py files or a JSON predictions file.

Usage:
    python py_to_step.py --input_dir ./results --suffix _31 --workers 8
    python py_to_step.py --input_dir ./results --suffix _31 --validate --output_dir ./valid_steps
    python py_to_step.py --input_json predictions.json --output_dir ./step_outputs --workers 8
"""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

_RUNNER = """
import sys
from pathlib import Path
from OCC.Core.BRepCheck import BRepCheck_Analyzer
import cadquery as cq

py_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
validate = sys.argv[3] == 'true'

ns = {}
exec(py_path.read_text(), ns)

result = ns.get('result') or ns.get('solid') or ns.get('shape') or ns.get('part')
if result is None:
    import ast
    try:
        tree = ast.parse(py_path.read_text())
        last_var = None
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        last_var = t.id
        if last_var and last_var in ns:
            result = ns[last_var]
    except Exception:
        pass

if result is None:
    print('ERROR: no result variable', file=sys.stderr); sys.exit(1)

if validate:
    shape = result.val() if hasattr(result, 'val') else result
    wrapped = shape.wrapped if hasattr(shape, 'wrapped') else shape
    analyzer = BRepCheck_Analyzer(wrapped)
    if not analyzer.IsValid():
        print('ERROR: BRepCheck failed', file=sys.stderr); sys.exit(2)

cq.exporters.export(result, str(out_path))
"""


def convert_one(args):
    file_id, py_path, out_step, validate, timeout = args
    if Path(out_step).exists():
        return file_id, "skipped", ""
    try:
        r = subprocess.run(
            [sys.executable, "-c", _RUNNER, str(py_path), str(out_step), str(validate).lower()],
            capture_output=True, text=True, timeout=timeout
        )
        if r.returncode == 0 and Path(out_step).exists():
            return file_id, "ok", ""
        err = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else f"exit {r.returncode}"
        return file_id, "failed", err
    except subprocess.TimeoutExpired:
        return file_id, "timeout", f">{timeout}s"
    except Exception as e:
        return file_id, "error", str(e)
    finally:
        # clean up temp .py if it was written from JSON
        pass


def load_from_dir(input_dir: Path, suffix: str, skip_existing: bool, output_dir: Path):
    tasks = []
    for py in sorted(input_dir.glob(f"*{suffix}.py")):
        file_id = py.stem
        out_step = output_dir / f"{file_id}.step"
        if skip_existing and out_step.exists():
            continue
        tasks.append((file_id, py, out_step))
    return tasks


def load_from_json(input_json: Path, output_dir: Path, skip_existing: bool, tmp_dir: Path):
    data = json.load(open(input_json))
    preds = data.get("predictions", data) if isinstance(data, dict) else data
    tasks = []
    for entry in preds:
        file_id = entry.get("file_id", "unknown")
        code = entry.get("generated") or entry.get("code", "")
        if not code or not code.strip():
            continue
        out_step = output_dir / f"{file_id}_gen.step"
        if skip_existing and out_step.exists():
            continue
        tmp_py = tmp_dir / f"{file_id}_tmp.py"
        tmp_py.write_text(code)
        tasks.append((file_id, tmp_py, out_step))
    return tasks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir",  default=None, help="Directory with CadQuery .py files")
    parser.add_argument("--input_json", default=None, help="JSON predictions file with 'file_id' and 'generated'")
    parser.add_argument("--output_dir", default=None, help="Where to save STEP files (default: {input_dir}_step/)")
    parser.add_argument("--suffix",     default="_31",  help="Suffix to match .py files (dir mode)")
    parser.add_argument("--validate",   action="store_true", help="Run BRepCheck topology validation")
    parser.add_argument("--workers",    type=int, default=8)
    parser.add_argument("--timeout",    type=int, default=30)
    parser.add_argument("--skip_existing", action="store_true", default=True)
    parser.add_argument("--failures_tsv",  default=None, help="Write failed conversions to TSV")
    args = parser.parse_args()

    if not args.input_dir and not args.input_json:
        parser.error("Provide --input_dir or --input_json")

    if args.input_dir:
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir) if args.output_dir else Path(str(input_dir) + "_step")
        output_dir.mkdir(parents=True, exist_ok=True)
        tasks = load_from_dir(input_dir, args.suffix, args.skip_existing, output_dir)
    else:
        input_json = Path(args.input_json)
        output_dir = Path(args.output_dir or "step_outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        tasks = load_from_json(input_json, output_dir, args.skip_existing, output_dir)

    print(f"Converting {len(tasks)} files  (validate={args.validate}, workers={args.workers})")

    ok = failed = skipped = 0
    failures = []

    with ProcessPoolExecutor(max_workers=args.workers) as exe:
        futures = {exe.submit(convert_one, (fid, py, step, args.validate, args.timeout)): fid
                   for fid, py, step in tasks}
        for i, fut in enumerate(as_completed(futures), 1):
            fid, status, err = fut.result()
            if status == "ok":      ok += 1
            elif status == "skipped": skipped += 1
            else:
                failed += 1
                failures.append((fid, err))
            if i % 500 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ok={ok} failed={failed} skipped={skipped}")

    print(f"\nDone: {ok} ok, {failed} failed, {skipped} skipped")
    print(f"Output: {output_dir}")

    if args.failures_tsv and failures:
        Path(args.failures_tsv).write_text("\n".join(f"{fid}\t{err}" for fid, err in failures))
        print(f"Failures written to: {args.failures_tsv}")

    # clean up temp py files from JSON mode
    if args.input_json:
        for _, py, _ in tasks:
            if "_tmp.py" in py.name:
                py.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
