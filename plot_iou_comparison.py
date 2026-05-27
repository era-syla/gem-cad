"""Quick IOU comparison bar chart: Gemini 3.0 vs 3.1"""

import matplotlib.pyplot as plt
import numpy as np

models = ["Gemini 3.0", "Gemini 3.1"]
ious = [57.0, 69.0]
colors = ["#4ECDC4", "#FF6B6B"]

fig, ax = plt.subplots(figsize=(6, 5))

bars = ax.bar(models, ious, color=colors, edgecolor="black", width=0.45)

for bar, val in zip(bars, ious):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.0,
        f"{val:.0f}%",
        ha="center", va="bottom", fontsize=14, fontweight="bold"
    )

ax.set_ylabel("Mean IOU (%)", fontsize=12)
ax.set_title("IOU Score Comparison\n(n=20 samples)", fontsize=13)
ax.set_ylim(0, 100)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))

# Annotate improvement arrow
ax.annotate(
    "+12%",
    xy=(1, ious[1] / 2 + 5),
    xytext=(0, ious[0] / 2 + 5),
    arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
    ha="center", fontsize=11, color="black"
)

plt.tight_layout()
out = "iou_comparison.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Saved: {out}")
