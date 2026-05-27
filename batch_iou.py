"""Compute IOU scores for all generated STEP files vs ground truth.

Usage:
    conda activate iou-env
    python batch_iou.py --input_dir ./sketch_extrude_easy --suffix _31
    python batch_iou.py --input_dir ./sketch_extrude_easy --suffix _31_med
"""

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

_RUNNER = """
import warnings
warnings.filterwarnings('ignore')
import sys
from iou import load_step_file, align_shapes
gt_path, gen_path = sys.argv[1], sys.argv[2]
gt_shape = load_step_file(gt_path)
gen_shape = load_step_file(gen_path)
_, iou = align_shapes(gen_shape, gt_shape)
print(iou)
"""


def find_pairs(input_dir: Path, suffix: str, gen_dir: Path = None):
    """Find (ground_truth, generated) STEP file pairs.
    If gen_dir is set, generated files are looked up there; gt files in input_dir.
    """
    if gen_dir is None:
        gen_dir = input_dir
    pairs = []
    for gt_path in sorted(input_dir.glob("*.step")):
        if gt_path.stem.endswith(suffix):
            continue  # skip generated files if in same dir
        gen_path = gen_dir / f"{gt_path.stem}{suffix}.step"
        if gen_path.exists():
            pairs.append((gt_path, gen_path))
    return pairs


def compute_pair(gt_path: Path, gen_path: Path, timeout: int):
    key = gen_path.stem
    try:
        proc = subprocess.run(
            [sys.executable, "-c", _RUNNER, str(gt_path), str(gen_path)],
            capture_output=True, text=True, timeout=timeout
        )
        if proc.returncode == 0:
            iou = float(proc.stdout.strip())
            return key, iou, None
        error = proc.stderr.strip().split("\n")[-1] if proc.stderr else "non-zero exit"
        return key, None, error
    except subprocess.TimeoutExpired:
        return key, None, f"timeout after {timeout}s"
    except Exception as e:
        return key, None, str(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--gen_dir", type=str, default=None, help="Directory with generated STEP files (defaults to input_dir)")
    parser.add_argument("--suffix", type=str, default="_31")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=60, help="Max seconds per pair before skipping")
    parser.add_argument("--output", type=str, default=None, help="Save scores to a JSON file")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    gen_dir = Path(args.gen_dir) if args.gen_dir else None
    pairs = find_pairs(input_dir, args.suffix, gen_dir)
    print(f"Found {len(pairs)} pairs for suffix '{args.suffix}'")

    if args.samples:
        pairs = pairs[:args.samples]
        print(f"Limited to {len(pairs)} samples")
    print()

    scores = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(compute_pair, gt, gen, args.timeout): gen.stem for gt, gen in pairs}
        for future in as_completed(futures):
            key, iou, error = future.result()
            if error:
                print(f"[{key}] ERROR: {error}")
                scores[key] = None
            else:
                print(f"[{key}] IOU = {iou:.4f} ({iou*100:.1f}%)")
                scores[key] = iou

    # Summary
    valid = [v for v in scores.values() if v is not None and v > 0]
    print("=" * 50)
    print(f"Suffix: {args.suffix}")
    print(f"Pairs evaluated: {len(valid)} / {len(pairs)}")
    if valid:
        print(f"Mean IOU:  {sum(valid)/len(valid):.4f}")
        print(f"Min IOU:   {min(valid):.4f}")
        print(f"Max IOU:   {max(valid):.4f}")

    if args.output:
        out_path = Path(args.output)
        with open(out_path, "w") as f:
            json.dump(scores, f, indent=2)
        print(f"Scores saved to {out_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
