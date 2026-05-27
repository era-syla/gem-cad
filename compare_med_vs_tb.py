"""Compare MEDIUM vs thinkingBudget 2048 on the same 50 images (skip 100)."""

import re
from pathlib import Path

import cadquery as cq
from OCP.TopAbs import TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
import matplotlib.pyplot as plt
import numpy as np


def count_faces(step_path: Path) -> int | None:
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
        print(f"  ERROR: {step_path.name}: {e}")
        return None


def extract_base_id(filename: str) -> str:
    name = filename.replace(".step", "").replace(".py", "")
    name = re.sub(r"_31(_med|_tb2048|_low)?$", "", name)
    return name


input_dir = Path("./new_batch")

# Only compare the skip-100 batch (IDs >= 00019635)
suffixes = {
    "MEDIUM": "_31_med",
    "TB2048": "_31_tb2048",
}

# Collect .py and .step files for each
py_files = {}
step_files = {}
for level, suffix in suffixes.items():
    all_py = sorted(input_dir.glob(f"*{suffix}.py"))
    all_step = sorted(input_dir.glob(f"*{suffix}.step"))
    # Filter to skip-100 batch only (IDs starting with 00019 or higher)
    py_files[level] = [f for f in all_py if f.name[:5] >= "00019"]
    step_files[level] = [f for f in all_step if f.name[:5] >= "00019"]

print("=" * 60)
print("STEP CONVERSION SUCCESS (skip-100 batch only)")
print("=" * 60)
for level in suffixes:
    n_py = len(py_files[level])
    n_step = len(step_files[level])
    rate = n_step / n_py * 100 if n_py > 0 else 0
    print(f"  {level:>8}: {n_step}/{n_py} = {rate:.0f}%")

# Count faces
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

# Find common samples
common = sorted(set(face_counts["MEDIUM"].keys()) & set(face_counts["TB2048"].keys()))
print(f"\n{len(common)} samples with valid STEP in both settings")

# Summary
print(f"\n{'=' * 60}")
print("FACE COUNT SUMMARY")
print("=" * 60)
for level in suffixes:
    counts = list(face_counts[level].values())
    if counts:
        print(f"  {level:>8}: n={len(counts)}, avg={np.mean(counts):.1f}, "
              f"median={np.median(counts):.1f}, std={np.std(counts):.1f}, "
              f"min={min(counts)}, max={max(counts)}")

# Common samples only
print(f"\n  --- Common samples ({len(common)}) ---")
for level in suffixes:
    counts = [face_counts[level][cid] for cid in common]
    print(f"  {level:>8}: avg={np.mean(counts):.1f}, median={np.median(counts):.1f}")

# Token data from actual runs
med_tokens = {"input": 1192, "output": 506, "think": 5458}  # from 50-sample run
# TB2048: user pasted partial output showing think values often exceeding 2048
# From visible samples: think ranged 0-14095 with many >2048
# We don't have the summary, so estimate from visible data
tb_think_visible = [9213, 8781, 5773, 4856, 7678, 5516, 5437, 14095, 5701, 0, 1926, 1088, 327, 5490, 3154, 3293, 1944]
tb_avg_think = int(np.mean(tb_think_visible))
tb_tokens = {"input": 1192, "output": 550, "think": tb_avg_think}  # output estimated

INPUT_PRICE = 2.50
OUTPUT_PRICE = 15.00

# --- Generate table PNG ---
fig, axes = plt.subplots(3, 1, figsize=(11, 10))

# Table 1: Token comparison
ax1 = axes[0]
ax1.axis("off")
ax1.set_title("Token Usage Comparison (per sample averages)", fontsize=14, fontweight="bold", pad=20)

col_labels1 = ["Input", "Output", "Thinking", "Total", "Per Sample Cost"]
row_labels1 = ["MEDIUM", "Budget 2048"]
cell_text1 = []
for label, tok in [("MEDIUM", med_tokens), ("Budget 2048", tb_tokens)]:
    total = tok["input"] + tok["output"] + tok["think"]
    cost = tok["input"] / 1e6 * INPUT_PRICE + (tok["output"] + tok["think"]) / 1e6 * OUTPUT_PRICE
    cell_text1.append([
        f'{tok["input"]:,}', f'{tok["output"]:,}', f'{tok["think"]:,}',
        f'{total:,}', f'${cost:.4f}'
    ])

table1 = ax1.table(cellText=cell_text1, rowLabels=row_labels1, colLabels=col_labels1,
                    cellLoc="right", rowLoc="center", loc="center")
table1.auto_set_font_size(False)
table1.set_fontsize(11)
table1.scale(1.2, 1.8)
for j in range(len(col_labels1)):
    table1[0, j].set_facecolor("#2C3E50")
    table1[0, j].set_text_props(color="white", fontweight="bold")
# Highlight thinking column
table1[1, 2].set_facecolor("#FFD93D40")
table1[2, 2].set_facecolor("#4ECDC440")

# Table 2: STEP success + face counts
ax2 = axes[1]
ax2.axis("off")
ax2.set_title("Quality Comparison (skip-100 batch, same 50 images)", fontsize=14, fontweight="bold", pad=20)

col_labels2 = [".py Files", "Valid STEP", "Success %", "Avg Faces", "Median Faces"]
row_labels2 = ["MEDIUM", "Budget 2048"]
cell_text2 = []
for level, label in [("MEDIUM", "MEDIUM"), ("TB2048", "Budget 2048")]:
    n_py = len(py_files[level])
    n_step = len(step_files[level])
    rate = n_step / n_py * 100 if n_py > 0 else 0
    counts = list(face_counts[level].values())
    avg_f = np.mean(counts) if counts else 0
    med_f = np.median(counts) if counts else 0
    cell_text2.append([str(n_py), str(n_step), f"{rate:.0f}%", f"{avg_f:.1f}", f"{med_f:.0f}"])

table2 = ax2.table(cellText=cell_text2, rowLabels=row_labels2, colLabels=col_labels2,
                    cellLoc="right", rowLoc="center", loc="center")
table2.auto_set_font_size(False)
table2.set_fontsize(11)
table2.scale(1.2, 1.8)
for j in range(len(col_labels2)):
    table2[0, j].set_facecolor("#2C3E50")
    table2[0, j].set_text_props(color="white", fontweight="bold")

# Table 3: Projected 100k cost
ax3 = axes[2]
ax3.axis("off")
ax3.set_title("Projected Cost for 100k Samples", fontsize=14, fontweight="bold", pad=20)

col_labels3 = ["100k Standard", "100k Batch (50%)", "Savings vs MEDIUM"]
row_labels3 = ["MEDIUM", "Budget 2048"]
cell_text3 = []
costs = {}
for label, tok in [("MEDIUM", med_tokens), ("Budget 2048", tb_tokens)]:
    per = tok["input"] / 1e6 * INPUT_PRICE + (tok["output"] + tok["think"]) / 1e6 * OUTPUT_PRICE
    std = per * 100_000
    batch = std * 0.5
    costs[label] = batch
    cell_text3.append([f"${std:,.0f}", f"${batch:,.0f}", ""])

# Calculate savings
saving = (1 - costs["Budget 2048"] / costs["MEDIUM"]) * 100
cell_text3[0][2] = "baseline"
cell_text3[1][2] = f"{saving:+.0f}%"

table3 = ax3.table(cellText=cell_text3, rowLabels=row_labels3, colLabels=col_labels3,
                    cellLoc="right", rowLoc="center", loc="center")
table3.auto_set_font_size(False)
table3.set_fontsize(11)
table3.scale(1.2, 1.8)
for j in range(len(col_labels3)):
    table3[0, j].set_facecolor("#2C3E50")
    table3[0, j].set_text_props(color="white", fontweight="bold")
table3[2, 1].set_facecolor("#E8F6F3")
table3[2, 1].set_text_props(fontweight="bold")

plt.tight_layout()
plt.savefig(str(input_dir / "med_vs_tb2048_comparison.png"), dpi=150, bbox_inches="tight", facecolor="white")
print(f"\nPlot saved to {input_dir / 'med_vs_tb2048_comparison.png'}")
