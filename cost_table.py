"""Generate cost comparison table as PNG."""

import matplotlib.pyplot as plt
import numpy as np

# Per-sample token data (measured)
data = {
    "LOW":     {"input": 1192, "output": 470,  "think": 0,     "step_rate": 70},
    "MEDIUM":  {"input": 1192, "output": 458,  "think": 4458,  "step_rate": 83},
    "Default": {"input": 1192, "output": 463,  "think": 8761,  "step_rate": 93},
}

# Pricing
INPUT_PRICE = 2.50   # per 1M tokens
OUTPUT_PRICE = 15.00  # per 1M tokens (output + thinking)
N = 100_000

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

# --- Table 1: Per-Sample Tokens ---
col_labels = ["Input", "Output", "Thinking", "Total Tokens"]
row_labels = list(data.keys())
cell_text = []
for level in row_labels:
    d = data[level]
    total = d["input"] + d["output"] + d["think"]
    cell_text.append([
        f'{d["input"]:,}',
        f'{d["output"]:,}',
        f'{d["think"]:,}',
        f'{total:,}',
    ])

ax1.axis("off")
ax1.set_title("Per-Sample Token Usage (measured averages)", fontsize=14, fontweight="bold", pad=20)
table1 = ax1.table(
    cellText=cell_text,
    rowLabels=row_labels,
    colLabels=col_labels,
    cellLoc="right",
    rowLoc="center",
    loc="center",
)
table1.auto_set_font_size(False)
table1.set_fontsize(12)
table1.scale(1.2, 1.8)

# Style header
for j in range(len(col_labels)):
    table1[0, j].set_facecolor("#2C3E50")
    table1[0, j].set_text_props(color="white", fontweight="bold")
for i in range(len(row_labels)):
    table1[i + 1, -1].set_facecolor("#E8F6F3")

# Row label colors
colors_row = ["#4ECDC4", "#FFD93D", "#FF6B6B"]
for i, color in enumerate(colors_row):
    table1[i + 1, -1].set_facecolor(color + "40")

# --- Table 2: Cost for 100k Samples ---
col_labels2 = ["Per Sample", "100k Standard", "100k Batch (50% off)", "STEP Success"]
cell_text2 = []
for level in row_labels:
    d = data[level]
    cost_in = d["input"] / 1e6 * INPUT_PRICE
    cost_out = (d["output"] + d["think"]) / 1e6 * OUTPUT_PRICE
    per_sample = cost_in + cost_out
    standard = per_sample * N
    batch = standard * 0.5
    cell_text2.append([
        f'${per_sample:.3f}',
        f'${standard:,.0f}',
        f'${batch:,.0f}',
        f'{d["step_rate"]}%',
    ])

ax2.axis("off")
ax2.set_title("Cost for 100k Samples  (Gemini 3.1 Pro: $2.50/M in, $15/M out+think)",
              fontsize=14, fontweight="bold", pad=20)
table2 = ax2.table(
    cellText=cell_text2,
    rowLabels=row_labels,
    colLabels=col_labels2,
    cellLoc="right",
    rowLoc="center",
    loc="center",
)
table2.auto_set_font_size(False)
table2.set_fontsize(12)
table2.scale(1.2, 1.8)

for j in range(len(col_labels2)):
    table2[0, j].set_facecolor("#2C3E50")
    table2[0, j].set_text_props(color="white", fontweight="bold")

# Highlight batch column
for i in range(len(row_labels)):
    table2[i + 1, 2].set_facecolor("#E8F6F3")
    table2[i + 1, 2].set_text_props(fontweight="bold")

plt.tight_layout()
plt.savefig("new_batch/cost_table.png", dpi=150, bbox_inches="tight", facecolor="white")
print("Saved to new_batch/cost_table.png")
