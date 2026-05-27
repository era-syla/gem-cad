"""Compute IOU between ground truth and predicted STEP files.

Usage:
    python batch_iou_orcd.py \
        --gt_dir /orcd/data/faez/001/era/bench0_steps \
        --pred_dir /orcd/data/faez/001/era/step_outputs/annie_gemcad_scaled_imonly \
        --output results_annie_gemcad.json \
        --workers 8

GT files expected as:    {file_id}.step
Predicted files expected: {file_id}_gen.step  (or {file_id}.step)

Outputs a JSON with per-sample IOU and summary stats.
"""

import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

_IOU_SCRIPT = """
import sys
sys.path.insert(0, '{iou_dir}')
from iou import load_step_file, align_shapes
try:
    s_gen = load_step_file(sys.argv[1])
    s_gt  = load_step_file(sys.argv[2])
    _, iou = align_shapes(s_gen, s_gt)
    print(iou)
except Exception as e:
    print(f'ERROR: {{e}}', file=sys.stderr)
    sys.exit(1)
"""


def compute_iou(args):
    file_id, pred_step, gt_step, iou_dir, timeout = args
    script = _IOU_SCRIPT.format(iou_dir=iou_dir)
    try:
        r = subprocess.run(
            [sys.executable, "-c", script, str(pred_step), str(gt_step)],
            capture_output=True, text=True, timeout=timeout
        )
        if r.returncode == 0 and r.stdout.strip():
            line = r.stdout.strip().splitlines()[-1]
            return file_id, float(line), None
        err = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else f"exit {r.returncode}"
        return file_id, None, err
    except subprocess.TimeoutExpired:
        return file_id, None, f"timeout >{timeout}s"
    except Exception as e:
        return file_id, None, str(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gt_dir",   required=True, help="Dir with ground truth .step files")
    parser.add_argument("--pred_dir", required=True, help="Dir with predicted .step files")
    parser.add_argument("--output",   required=True, help="Output JSON path")
    parser.add_argument("--workers",  type=int, default=4)
    parser.add_argument("--timeout",  type=int, default=60)
    parser.add_argument("--iou_script", default=None,
                        help="Directory containing iou.py (default: same dir as this script)")
    args = parser.parse_args()

    iou_dir = args.iou_script or str(Path(__file__).parent)
    gt_dir   = Path(args.gt_dir)
    pred_dir = Path(args.pred_dir)

    # Build GT lookup: file_id -> path
    gt_map = {}
    for f in gt_dir.glob("*.step"):
        gt_map[f.stem] = f

    # Build predicted lookup: strip _gen suffix if present
    pred_map = {}
    for f in pred_dir.glob("*.step"):
        stem = f.stem
        fid = stem[:-4] if stem.endswith("_gen") else stem
        pred_map[fid] = f

    # Find matching pairs
    common = sorted(set(gt_map) & set(pred_map))
    only_gt   = len(gt_map) - len(common)
    only_pred = len(pred_map) - len(common)
    print(f"GT files:   {len(gt_map)}")
    print(f"Pred files: {len(pred_map)}")
    print(f"Pairs:      {len(common)}  (gt_only={only_gt}, pred_only={only_pred})")

    tasks = [(fid, pred_map[fid], gt_map[fid], iou_dir, args.timeout) for fid in common]

    results = {}
    errors  = {}
    with ProcessPoolExecutor(max_workers=args.workers) as exe:
        futures = {exe.submit(compute_iou, t): t[0] for t in tasks}
        for i, fut in enumerate(as_completed(futures), 1):
            fid, iou, err = fut.result()
            if iou is not None:
                results[fid] = iou
            else:
                errors[fid] = err
            if i % 100 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  computed={len(results)} errors={len(errors)}")

    scores = list(results.values())
    total_pred = len(pred_map)
    summary = {
        "total_gt":        len(gt_map),
        "total_pred":      total_pred,
        "pairs":           len(common),
        "iou_computed":    len(scores),
        "iou_errors":      len(errors),
        "valid_rate":      round(len(scores) / total_pred * 100, 2) if total_pred else 0,
        "mean_iou":        round(statistics.mean(scores), 4) if scores else None,
        "median_iou":      round(statistics.median(scores), 4) if scores else None,
        "min_iou":         round(min(scores), 4) if scores else None,
        "max_iou":         round(max(scores), 4) if scores else None,
    }

    output = {
        "summary": summary,
        "per_sample": results,
        "errors": errors,
    }

    Path(args.output).write_text(json.dumps(output, indent=2))

    print(f"\n=== SUMMARY ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
