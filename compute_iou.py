"""Compute IOU between ground truth and generated STEP files.

Supports two modes:
  - Same directory: GT and generated files in the same dir, matched by suffix
  - Separate directories: GT in --gt_dir, predictions in --pred_dir (expects {file_id}_gen.step)

Usage:
    python compute_iou.py --input_dir ./bench0_steps --suffix _31 --output scores.json
    python compute_iou.py --gt_dir ./gt_steps --pred_dir ./pred_steps --output scores.json --workers 8
"""

import argparse
import json
import statistics
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

_RUNNER = """
import warnings, sys
warnings.filterwarnings('ignore')
sys.path.insert(0, '{iou_dir}')
from iou import load_step_file, align_shapes
s_gen = load_step_file(sys.argv[1])
s_gt  = load_step_file(sys.argv[2])
_, iou = align_shapes(s_gen, s_gt)
print(iou)
"""


def compute_pair(args):
    file_id, pred_step, gt_step, iou_dir, timeout = args
    script = _RUNNER.format(iou_dir=iou_dir)
    try:
        r = subprocess.run(
            [sys.executable, "-c", script, str(pred_step), str(gt_step)],
            capture_output=True, text=True, timeout=timeout
        )
        if r.returncode == 0 and r.stdout.strip():
            return file_id, float(r.stdout.strip().splitlines()[-1]), None
        err = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else f"exit {r.returncode}"
        return file_id, None, err
    except subprocess.TimeoutExpired:
        return file_id, None, f"timeout >{timeout}s"
    except Exception as e:
        return file_id, None, str(e)


def find_pairs_same_dir(input_dir: Path, suffix: str):
    pairs = []
    for gt in sorted(input_dir.glob("*.step")):
        if gt.stem.endswith(suffix): continue
        pred = input_dir / f"{gt.stem}{suffix}.step"
        if pred.exists():
            pairs.append((gt.stem, pred, gt))
    return pairs


def find_pairs_separate_dirs(gt_dir: Path, pred_dir: Path):
    gt_map   = {f.stem: f for f in gt_dir.glob("*.step")}
    pred_map = {}
    for f in pred_dir.glob("*.step"):
        fid = f.stem[:-4] if f.stem.endswith("_gen") else f.stem
        pred_map[fid] = f
    common = sorted(set(gt_map) & set(pred_map))
    return [(fid, pred_map[fid], gt_map[fid]) for fid in common]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", default=None, help="Dir with both GT and generated STEP files")
    parser.add_argument("--gt_dir",    default=None, help="Dir with ground truth STEP files")
    parser.add_argument("--pred_dir",  default=None, help="Dir with predicted STEP files ({id}_gen.step)")
    parser.add_argument("--suffix",    default="_31", help="Suffix for generated files (same-dir mode)")
    parser.add_argument("--output",    default=None, help="Save results to JSON")
    parser.add_argument("--workers",   type=int, default=8)
    parser.add_argument("--timeout",   type=int, default=60)
    parser.add_argument("--samples",   type=int, default=None)
    parser.add_argument("--iou_script", default=None, help="Dir containing iou.py")
    args = parser.parse_args()

    iou_dir = args.iou_script or str(Path(__file__).parent)

    if args.input_dir:
        pairs = find_pairs_same_dir(Path(args.input_dir), args.suffix)
        total_gt = len(list(Path(args.input_dir).glob("*.step")))
    elif args.gt_dir and args.pred_dir:
        pairs = find_pairs_separate_dirs(Path(args.gt_dir), Path(args.pred_dir))
        total_gt = len(list(Path(args.gt_dir).glob("*.step")))
        total_pred = len(list(Path(args.pred_dir).glob("*.step")))
        print(f"GT files:   {total_gt}")
        print(f"Pred files: {total_pred}")
    else:
        parser.error("Provide either --input_dir or both --gt_dir and --pred_dir")

    print(f"Pairs:      {len(pairs)}")
    if args.samples:
        pairs = pairs[:args.samples]

    tasks = [(fid, pred, gt, iou_dir, args.timeout) for fid, pred, gt in pairs]
    results, errors = {}, {}

    with ProcessPoolExecutor(max_workers=args.workers) as exe:
        futures = {exe.submit(compute_pair, t): t[0] for t in tasks}
        for i, fut in enumerate(as_completed(futures), 1):
            fid, iou, err = fut.result()
            if iou is not None:
                results[fid] = iou
            else:
                errors[fid] = err
            if i % 100 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}  computed={len(results)} errors={len(errors)}")

    scores = list(results.values())
    total_pred = total_pred if args.gt_dir else total_gt
    summary = {
        "pairs":        len(pairs),
        "iou_computed": len(scores),
        "iou_errors":   len(errors),
        "valid_rate":   round(len(scores) / total_pred * 100, 2) if total_pred else 0,
        "mean_iou":     round(statistics.mean(scores), 4) if scores else None,
        "median_iou":   round(statistics.median(scores), 4) if scores else None,
        "min_iou":      round(min(scores), 4) if scores else None,
        "max_iou":      round(max(scores), 4) if scores else None,
    }

    print("\n=== SUMMARY ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    if args.output:
        Path(args.output).write_text(json.dumps({"summary": summary, "per_sample": results, "errors": errors}, indent=2))
        print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
