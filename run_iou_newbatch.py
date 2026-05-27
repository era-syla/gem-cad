"""Compute IOU for new_batch samples vs ground truth in abc-rendering."""

import sys
sys.path.insert(0, "/Users/erasyla/gem-cad")

from iou import load_step_file, align_shapes
from pathlib import Path

GT_BASE = Path("/Users/erasyla/abc-rendering/new_batch_steps")
GEN_BASE = Path("/Users/erasyla/gem-cad/new_batch")

PAIRS = [
    ("00000941", "00000941_f297a24e1a4446cf9d74efd9_step_000"),
    ("00001067", "00001067_8a2edcf36bcd435092f4c8ae_step_001"),
    ("00001250", "00001250_96503b6a26c64074ad598927_step_012"),
    ("00001485", "00001485_a45f6c99e2154f3b94955175_step_069"),
]

SUFFIXES = {"3.0": "_0_30", "3.1": "_0_31"}

results = {k: [] for k in SUFFIXES}

for short_id, base in PAIRS:
    gt_path = GT_BASE / short_id / f"{base}.step"
    print(f"\n[{short_id}]  gt: {gt_path.name}")
    try:
        gt_shape = load_step_file(str(gt_path))
    except Exception as e:
        print(f"  ERROR loading GT: {e}")
        continue

    for model, suf in SUFFIXES.items():
        gen_path = GEN_BASE / f"{base}{suf}.step"
        if not gen_path.exists():
            print(f"  {model}: MISSING {gen_path.name}")
            continue
        try:
            gen_shape = load_step_file(str(gen_path))
            _, iou = align_shapes(gen_shape, gt_shape)
            scaled = iou * 2
            results[model].append(iou)
            print(f"  {model}: {gen_path.name}  →  IOU×2 = {scaled:.4f} ({scaled*100:.1f}%)")
        except Exception as e:
            print(f"  {model}: ERROR — {e}")

print("\n" + "=" * 55)
print(f"{'Model':<10} {'n':>4}  {'Mean IOU×2':>12}  {'Min':>8}  {'Max':>8}")
print("-" * 55)
for model, scores in results.items():
    if scores:
        scaled = [s * 2 for s in scores]
        print(f"{'Gemini '+model:<10} {len(scores):>4}  {sum(scaled)/len(scaled)*100:>11.1f}%  "
              f"{min(scaled)*100:>7.1f}%  {max(scaled)*100:>7.1f}%")
    else:
        print(f"{'Gemini '+model:<10} {'—':>4}")
print("=" * 55)
