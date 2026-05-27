"""Convert generated CadQuery code from prediction JSON files to STEP files.

Usage:
    python json_to_step.py --input path/to/predictions.json --output_dir ./step_outputs
    python json_to_step.py --input path/to/predictions.json --output_dir ./step_outputs --workers 8

Each entry in the JSON must have a 'file_id' and 'generated' field.
Outputs are saved as {file_id}_gen.step in output_dir.
"""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

_RUNNER = """
import sys, cadquery as cq
from pathlib import Path
ns = {}
exec(Path(sys.argv[1]).read_text(), ns)
result = ns.get('result') or ns.get('solid') or ns.get('shape') or ns.get('part')
if result is None:
    import ast
    tree = ast.parse(Path(sys.argv[1]).read_text())
    last_var = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    last_var = t.id
    if last_var and last_var in ns:
        result = ns[last_var]
if result is None:
    print('ERROR: no result variable', file=sys.stderr); sys.exit(1)
cq.exporters.export(result, sys.argv[2])
"""


def convert_entry(args):
    file_id, code, out_dir, timeout = args
    out_step = Path(out_dir) / f"{file_id}_gen.step"
    if out_step.exists():
        return file_id, "skipped", ""
    if not code or not code.strip():
        return file_id, "empty", ""
    tmp_py = Path(out_dir) / f"{file_id}_gen.py"
    tmp_py.write_text(code)
    try:
        r = subprocess.run(
            [sys.executable, "-c", _RUNNER, str(tmp_py), str(out_step)],
            capture_output=True, text=True, timeout=timeout
        )
        if r.returncode == 0 and out_step.exists():
            return file_id, "ok", ""
        err = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "unknown"
        return file_id, "failed", err
    except subprocess.TimeoutExpired:
        return file_id, "timeout", f">{timeout}s"
    finally:
        tmp_py.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to predictions JSON file")
    parser.add_argument("--output_dir", required=True, help="Directory for output STEP files")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per script (seconds)")
    parser.add_argument("--skip_existing", action="store_true", default=True)
    args = parser.parse_args()

    data = json.load(open(args.input))
    preds = data.get("predictions", data) if isinstance(data, dict) else data

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tasks = [(e["file_id"], e.get("generated", ""), str(out_dir), args.timeout) for e in preds]
    print(f"Total entries: {len(tasks)}")

    ok = failed = skipped = empty = 0
    with ProcessPoolExecutor(max_workers=args.workers) as exe:
        futures = {exe.submit(convert_entry, t): t[0] for t in tasks}
        for i, fut in enumerate(as_completed(futures), 1):
            file_id, status, err = fut.result()
            if status == "ok": ok += 1
            elif status == "skipped": skipped += 1
            elif status == "empty": empty += 1
            else:
                failed += 1
                if failed <= 10:
                    print(f"  FAIL {file_id}: {err}")
            if i % 200 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  ok={ok} failed={failed} skipped={skipped}")

    print(f"\nDone: {ok} ok, {failed} failed, {skipped} skipped, {empty} empty")
    print(f"STEP files saved to: {out_dir}")


if __name__ == "__main__":
    main()
