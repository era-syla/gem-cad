"""Analyze token usage across all batch jobs and plot distribution."""

import json
import os
import matplotlib.pyplot as plt
import numpy as np
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Collect per-job stats
jobs_data = []
all_output_tokens = []

for job in client.batches.list():
    name = job.name
    state = job.state.name
    model = getattr(job, "model", "?")
    if state != "JOB_STATE_SUCCEEDED":
        jobs_data.append({"name": name, "state": state, "model": model,
                          "input": 0, "output": 0, "thinking": 0, "total": 0, "requests": 0})
        continue

    content = client.files.download(file=job.dest.file_name).decode("utf-8")
    j_in, j_out, j_think, j_count = 0, 0, 0, 0
    for line in content.splitlines():
        if not line.strip():
            continue
        parsed = json.loads(line)
        um = parsed.get("response", {}).get("usageMetadata", {})
        out_tokens = um.get("candidatesTokenCount", 0)
        j_in += um.get("promptTokenCount", 0)
        j_out += out_tokens
        j_think += um.get("thoughtsTokenCount", 0)
        j_count += 1
        if out_tokens > 0:
            all_output_tokens.append(out_tokens)

    jobs_data.append({
        "name": name, "state": state, "model": model,
        "input": j_in, "output": j_out, "thinking": j_think,
        "total": j_in + j_out + j_think, "requests": j_count,
    })

# Print table
print(f"\n{'Job':<20} {'Model':<25} {'Requests':>8} {'Input':>10} {'Output':>10} {'Thinking':>12} {'Total':>12}")
print("-" * 100)
grand_in, grand_out, grand_think = 0, 0, 0
for j in jobs_data:
    short_name = j["name"].split("/")[-1][:18]
    print(f"{short_name:<20} {str(j['model']):<25} {j['requests']:>8} {j['input']:>10,} {j['output']:>10,} {j['thinking']:>12,} {j['total']:>12,}")
    grand_in += j["input"]
    grand_out += j["output"]
    grand_think += j["thinking"]

print("-" * 100)
print(f"{'TOTAL':<20} {'':<25} {'':<8} {grand_in:>10,} {grand_out:>10,} {grand_think:>12,} {grand_in+grand_out+grand_think:>12,}")

# Plot distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(all_output_tokens, bins=50, color="#4285F4", edgecolor="white", alpha=0.9)
axes[0].set_xlabel("Output Tokens")
axes[0].set_ylabel("Count")
axes[0].set_title("Output Token Distribution (All Batch Jobs)")
axes[0].axvline(np.median(all_output_tokens), color="red", linestyle="--", label=f"Median: {int(np.median(all_output_tokens))}")
axes[0].axvline(np.mean(all_output_tokens), color="orange", linestyle="--", label=f"Mean: {int(np.mean(all_output_tokens))}")
axes[0].legend()

# Per-job breakdown (stacked bar)
job_labels = [j["name"].split("/")[-1][:10] for j in jobs_data if j["total"] > 0]
inputs = [j["input"] for j in jobs_data if j["total"] > 0]
outputs = [j["output"] for j in jobs_data if j["total"] > 0]
thinkings = [j["thinking"] for j in jobs_data if j["total"] > 0]

x = np.arange(len(job_labels))
axes[1].bar(x, inputs, label="Input", color="#4285F4")
axes[1].bar(x, outputs, bottom=inputs, label="Output", color="#34A853")
axes[1].bar(x, thinkings, bottom=[i + o for i, o in zip(inputs, outputs)], label="Thinking", color="#EA4335")
axes[1].set_xlabel("Batch Job")
axes[1].set_ylabel("Tokens")
axes[1].set_title("Token Usage per Batch Job")
axes[1].set_xticks(x)
axes[1].set_xticklabels(job_labels, rotation=45, ha="right", fontsize=8)
axes[1].legend()

plt.tight_layout()
plt.savefig("token_analysis.png", dpi=150)
print(f"\nSaved chart to token_analysis.png")

# Save table as PNG
fig_table, ax_table = plt.subplots(figsize=(14, max(3, len(jobs_data) * 0.5 + 1.5)))
ax_table.axis("off")
ax_table.set_title("Batch Job Token Usage Summary", fontsize=14, fontweight="bold", pad=20)

# Map batch job names to the thinking budget that was used
thinking_budgets = {
    "zw7iewy2bh1edspj9bveh": "1024",       # 3071 images
    "3ims921e3j6fxnrh5xbs0": "16384",      # 57 images
    "zr3yq22fe37iyf1jbmkut": "16384",      # 57 images
    "j7xvvtdtn698hv7exnse9": "1024",       # 57 images
    "bgbdpz2z62kn8bb7wwwit": "0 (failed)",  # thinking=0 rejected
    "yrbfcybgarbqd82itw1zh": "default",     # first successful run
    "2ka5kll5kkyae0ir7rqng": "default (bad URI)",  # first run, bad file URIs
}

headers = ["Job", "Model", "Think Budget", "Requests", "Input", "Output", "Thinking", "Total"]
rows = []
for j in jobs_data:
    short_name = j["name"].split("/")[-1][:20]
    budget = thinking_budgets.get(short_name[:21], "?")
    # Try partial match
    if budget == "?":
        for k, v in thinking_budgets.items():
            if k in j["name"]:
                budget = v
                break
    rows.append([
        short_name, str(j["model"]), budget, f"{j['requests']:,}",
        f"{j['input']:,}", f"{j['output']:,}", f"{j['thinking']:,}", f"{j['total']:,}"
    ])
rows.append(["TOTAL", "", "", "",
             f"{grand_in:,}", f"{grand_out:,}", f"{grand_think:,}", f"{grand_in+grand_out+grand_think:,}"])

table = ax_table.table(cellText=rows, colLabels=headers, loc="center", cellLoc="right")
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.4)

# Style header
for col in range(len(headers)):
    table[0, col].set_facecolor("#4285F4")
    table[0, col].set_text_props(color="white", fontweight="bold")
    table[0, col].set_edgecolor("white")

# Style total row
for col in range(len(headers)):
    table[len(rows), col].set_facecolor("#E8F0FE")
    table[len(rows), col].set_text_props(fontweight="bold")

# Left-align Job and Model columns
for row in range(len(rows) + 1):
    for col in [0, 1]:
        table[row, col].set_text_props(ha="left")

table.auto_set_column_width(list(range(len(headers))))
fig_table.tight_layout()
fig_table.savefig("token_table.png", dpi=150, bbox_inches="tight")
print(f"Saved table to token_table.png")
