"""Analyze face counts across thinking levels and plot comparison.

Usage:
    python analyze_faces.py --input_dir ./new_batch
"""

import argparse
import re
from pathlib import Path

import cadquery as cq
from OCP.TopAbs import TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
import matplotlib.pyplot as plt
import numpy as np


def count_faces(step_path: Path) -> int | None:
    """Load a STEP file and count its faces."""
    try:
        shape = cq.importers.importStep(str(step_path))
        solid = shape.val().wrapped
        explorer = TopExp_Explorer(solid, TopAbs_FACE)
        count = 0
        while explorer.More():
            count += 1
            explorer.Next()
        return count
    except Exception as e:
        print(f"  ERROR loading {step_path.name}: {e}")
        return None


def extract_base_id(filename: str) -> str:
    """Extract the base sample ID from a filename, stripping the suffix."""
    # e.g. 00001619_3a08e9121f43473c9106e6f9_step_000_0_31_low.step -> 00001619_3a08e9121f43473c9106e6f9_step_000_0
    # Remove .step extension first
    name = filename.replace(".step", "")
    # Remove the suffix (_31, _31_low, _31_med, _30, etc.)
    name = re.sub(r"_31(_low|_med)?$", "", name)
    name = re.sub(r"_30$", "", name)
    return name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, default="./new_batch")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)

    suffixes = {
        "LOW": "_31_low.step",
        "MEDIUM": "_31_med.step",
        "Default": "_31.step",
    }

    # Collect STEP files per level
    step_files = {}
    for level, suffix in suffixes.items():
        pattern = f"*{suffix}"
        files = sorted(input_dir.glob(pattern))
        # For Default, exclude files that also match _low or _med
        if level == "Default":
            files = [f for f in files if not f.name.endswith("_low.step") and not f.name.endswith("_med.step")]
        step_files[level] = files

    # Also count .py files for success rate
    py_suffixes = {"LOW": "_31_low.py", "MEDIUM": "_31_med.py", "Default": "_31.py"}
    py_counts = {}
    for level, suffix in py_suffixes.items():
        pattern = f"*{suffix}"
        files = sorted(input_dir.glob(pattern))
        if level == "Default":
            files = [f for f in files if not f.name.endswith("_low.py") and not f.name.endswith("_med.py")
                     and not f.name.endswith("_dbg.py")]
        py_counts[level] = len(files)

    print("=" * 60)
    print("STEP CONVERSION SUCCESS RATES")
    print("=" * 60)
    for level in suffixes:
        n_py = py_counts[level]
        n_step = len(step_files[level])
        rate = n_step / n_py * 100 if n_py > 0 else 0
        print(f"  {level:>8}: {n_step}/{n_py} = {rate:.0f}%")

    # Count faces for each STEP file
    print(f"\n{'=' * 60}")
    print("COUNTING FACES...")
    print("=" * 60)

    face_counts = {}
    for level in suffixes:
        face_counts[level] = {}
        for f in step_files[level]:
            base_id = extract_base_id(f.name)
            fc = count_faces(f)
            if fc is not None:
                face_counts[level][base_id] = fc
                print(f"  {level:>8} | {f.name}: {fc} faces")

    # Summary statistics
    print(f"\n{'=' * 60}")
    print("FACE COUNT SUMMARY")
    print("=" * 60)
    for level in suffixes:
        counts = list(face_counts[level].values())
        if counts:
            avg = np.mean(counts)
            med = np.median(counts)
            std = np.std(counts)
            mn, mx = min(counts), max(counts)
            print(f"  {level:>8}: n={len(counts)}, avg={avg:.1f}, median={med:.1f}, "
                  f"std={std:.1f}, min={mn}, max={mx}")
        else:
            print(f"  {level:>8}: no valid STEP files")

    # Plot 1: Bar chart of average face counts + success rate
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    levels = list(suffixes.keys())
    colors = ["#4ECDC4", "#FFD93D", "#FF6B6B"]

    # Average face count
    avgs = [np.mean(list(face_counts[l].values())) if face_counts[l] else 0 for l in levels]
    stds = [np.std(list(face_counts[l].values())) if face_counts[l] else 0 for l in levels]
    n_valid = [len(face_counts[l]) for l in levels]

    bars1 = ax1.bar(levels, avgs, yerr=stds, color=colors, edgecolor="black", capsize=5)
    ax1.set_ylabel("Face Count")
    ax1.set_title("Average Face Count by Thinking Level")
    for bar, avg, n in zip(bars1, avgs, n_valid):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                 f"{avg:.0f}\n(n={n})", ha="center", va="bottom", fontsize=10)

    # Success rate
    rates = [len(step_files[l]) / py_counts[l] * 100 if py_counts[l] > 0 else 0 for l in levels]
    bars2 = ax2.bar(levels, rates, color=colors, edgecolor="black")
    ax2.set_ylabel("STEP Conversion Rate (%)")
    ax2.set_title("STEP Conversion Success Rate")
    ax2.set_ylim(0, 110)
    for bar, rate, n_step in zip(bars2, rates, [len(step_files[l]) for l in levels]):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f"{rate:.0f}%\n({n_step})", ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    plt.savefig(str(input_dir / "face_count_comparison.png"), dpi=150, bbox_inches="tight")
    print(f"\nPlot saved to {input_dir / 'face_count_comparison.png'}")

    # Plot 2: Per-sample comparison (paired samples only)
    common_ids = set(face_counts["LOW"].keys()) & set(face_counts["MEDIUM"].keys()) & set(face_counts["Default"].keys())
    if common_ids:
        common_ids = sorted(common_ids)
        print(f"\n{len(common_ids)} samples have valid STEP files across all 3 levels")

        fig2, ax3 = plt.subplots(figsize=(max(10, len(common_ids) * 0.5), 6))
        x = np.arange(len(common_ids))
        width = 0.25

        for i, (level, color) in enumerate(zip(levels, colors)):
            vals = [face_counts[level][cid] for cid in common_ids]
            ax3.bar(x + i * width, vals, width, label=level, color=color, edgecolor="black")

        short_labels = [cid.split("_")[0] for cid in common_ids]
        ax3.set_xticks(x + width)
        ax3.set_xticklabels(short_labels, rotation=45, ha="right", fontsize=8)
        ax3.set_ylabel("Face Count")
        ax3.set_title(f"Per-Sample Face Count Comparison ({len(common_ids)} common samples)")
        ax3.legend()
        plt.tight_layout()
        plt.savefig(str(input_dir / "face_count_per_sample.png"), dpi=150, bbox_inches="tight")
        print(f"Per-sample plot saved to {input_dir / 'face_count_per_sample.png'}")


if __name__ == "__main__":
    main()
