"""Analyze generated CadQuery code — distribution of code tokens (excluding comments)."""

import os
import re
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

IMAGE_DIR = Path("/Users/erasyla/abc-rendering/images")


def strip_comments(code: str) -> str:
    """Remove comment lines and inline comments, keep only code."""
    lines = []
    in_docstring = False
    for line in code.splitlines():
        stripped = line.strip()
        # Skip docstrings
        if '"""' in stripped or "'''" in stripped:
            count = stripped.count('"""') + stripped.count("'''")
            if in_docstring:
                in_docstring = False
                continue
            elif count == 1:
                in_docstring = True
                continue
            # Single-line docstring (open+close on same line)
        if in_docstring:
            continue
        # Skip full-line comments
        if stripped.startswith("#"):
            continue
        # Skip empty lines
        if not stripped:
            continue
        # Remove inline comments
        line_no_comment = re.sub(r'\s+#.*$', '', line)
        lines.append(line_no_comment)
    return "\n".join(lines)


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for code."""
    return max(1, len(text) // 4)


py_files = sorted(IMAGE_DIR.glob("*.py"))
print(f"Found {len(py_files)} .py files")

results = []
errors = []
for f in py_files:
    code = f.read_text()
    if code.startswith("# Error:"):
        errors.append(f.stem)
        continue
    code_only = strip_comments(code)
    tokens = estimate_tokens(code_only)
    lines = len(code_only.splitlines())
    chars = len(code_only)
    results.append({"name": f.stem, "tokens": tokens, "lines": lines, "chars": chars})

print(f"Valid code files: {len(results)}")
print(f"Error files: {len(errors)}")

tokens = [r["tokens"] for r in results]
lines = [r["lines"] for r in results]
chars = [r["chars"] for r in results]

print(f"\n--- CODE-ONLY STATS (no comments) ---")
print(f"{'Metric':<15} {'Min':>8} {'Max':>8} {'Mean':>8} {'Median':>8}")
print("-" * 50)
for name, vals in [("Est. Tokens", tokens), ("Lines", lines), ("Characters", chars)]:
    print(f"{name:<15} {min(vals):>8} {max(vals):>8} {int(np.mean(vals)):>8} {int(np.median(vals)):>8}")

# Buckets for lines of code
print(f"\n--- LINES OF CODE BUCKETS ---")
buckets = [(0, 10), (10, 25), (25, 50), (50, 100), (100, 200), (200, 500)]
for lo, hi in buckets:
    count = sum(1 for l in lines if lo <= l < hi)
    print(f"  {lo:>3}-{hi:<3} lines: {count}")

# Bottom 10
sorted_by_tokens = sorted(results, key=lambda r: r["tokens"])
print(f"\n--- BOTTOM 10 (smallest code) ---")
for r in sorted_by_tokens[:10]:
    print(f"  {r['tokens']:>5} tokens, {r['lines']:>3} lines — {r['name']}")

print(f"\n--- TOP 10 (largest code) ---")
for r in sorted_by_tokens[-10:]:
    print(f"  {r['tokens']:>5} tokens, {r['lines']:>3} lines — {r['name']}")

# Plot
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

axes[0].hist(tokens, bins=50, color="#34A853", edgecolor="white", alpha=0.9)
axes[0].set_xlabel("Estimated Tokens (code only)")
axes[0].set_ylabel("Count")
axes[0].set_title("Code Token Distribution (no comments)")
axes[0].axvline(np.median(tokens), color="red", linestyle="--", label=f"Median: {int(np.median(tokens))}")
axes[0].axvline(np.mean(tokens), color="orange", linestyle="--", label=f"Mean: {int(np.mean(tokens))}")
axes[0].legend()

axes[1].hist(lines, bins=50, color="#4285F4", edgecolor="white", alpha=0.9)
axes[1].set_xlabel("Lines of Code (no comments/blanks)")
axes[1].set_ylabel("Count")
axes[1].set_title("Lines of Code Distribution")
axes[1].axvline(np.median(lines), color="red", linestyle="--", label=f"Median: {int(np.median(lines))}")
axes[1].axvline(np.mean(lines), color="orange", linestyle="--", label=f"Mean: {int(np.mean(lines))}")
axes[1].legend()

axes[2].hist(chars, bins=50, color="#EA4335", edgecolor="white", alpha=0.9)
axes[2].set_xlabel("Characters (code only)")
axes[2].set_ylabel("Count")
axes[2].set_title("Character Count Distribution")
axes[2].axvline(np.median(chars), color="red", linestyle="--", label=f"Median: {int(np.median(chars))}")
axes[2].axvline(np.mean(chars), color="orange", linestyle="--", label=f"Mean: {int(np.mean(chars))}")
axes[2].legend()

plt.tight_layout()
plt.savefig("code_distribution.png", dpi=150)
print(f"\nSaved chart to code_distribution.png")
