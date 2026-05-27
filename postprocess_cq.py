"""
Postprocess CadQuery .py files:
  - Strip markdown fences (```python ... ```)
  - Remove all # comments
  - Remove show_object(...) and show(...) calls, including wrapping if-blocks
  - Remove exportStep / export_step / .step export calls
  - Fix double-dot syntax errors (e.g. ))..moveTo -> )).moveTo)

Usage:
    python postprocess_cq.py --input_dir ./gray_cad_1 --suffix _31 --inplace
    python postprocess_cq.py --input_dir ./gray_cad_1 --inplace
"""

import argparse
import re
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed


_SHOW_RE = re.compile(r"^\s*(show_object|show)\s*\(")
_EXPORT_RE = re.compile(
    r"^\s*("
    r".*\.exportStep\s*\("
    r"|.*\.export\s*\(\s*['\"].*\.step['\"]"
    r"|export_step\s*\("
    r"|exportStep\s*\("
    r")"
)


def strip_markdown_fences(source: str) -> str:
    """Remove ```python / ``` fences if present."""
    stripped = source.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines)
    return source


def fix_double_dots(source: str) -> str:
    """Fix ))..method -> )).method double-dot syntax errors."""
    return re.sub(r'\)\.\.([a-zA-Z_])', r').\1', source)


def remove_comments(source: str) -> str:
    """Strip all # comments line by line."""
    lines = []
    for line in source.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        if "#" in line:
            # Naive inline comment strip — avoids breaking strings in most cases
            in_single = False
            in_double = False
            for i, ch in enumerate(line):
                if ch == "'" and not in_double:
                    in_single = not in_single
                elif ch == '"' and not in_single:
                    in_double = not in_double
                elif ch == "#" and not in_single and not in_double:
                    line = line[:i].rstrip() + "\n"
                    break
        lines.append(line)
    return "".join(lines)


def remove_show_and_export(source: str) -> str:
    """Remove show/export lines and their wrapping if-blocks."""
    lines = source.splitlines(keepends=True)
    out = []
    skip_indent = None

    for line in lines:
        stripped = line.rstrip("\n")

        if skip_indent is not None:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() == "" or current_indent > skip_indent:
                continue
            else:
                skip_indent = None

        if re.match(r"^\s*if\s+.*\bshow_object\b.*:", stripped) or \
           re.match(r"^\s*if\s+.*\bshow\b\s*\(.*:", stripped) or \
           re.match(r"""^\s*if\s+['"]show_object['"]\s+in\s+""", stripped) or \
           re.match(r"""^\s*if\s+['"]show['"]\s+in\s+""", stripped):
            skip_indent = len(line) - len(line.lstrip())
            continue

        if _SHOW_RE.match(stripped):
            continue

        if _EXPORT_RE.match(stripped):
            continue

        out.append(line)

    return "".join(out)


def clean_blank_lines(source: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", source)


def postprocess(source: str) -> str:
    source = strip_markdown_fences(source)
    source = fix_double_dots(source)
    source = remove_comments(source)
    source = remove_show_and_export(source)
    source = clean_blank_lines(source)
    return source.strip() + "\n"


def process_file(py_path: Path, out_path: Path) -> tuple:
    try:
        source = py_path.read_text(encoding="utf-8", errors="replace")
        cleaned = postprocess(source)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(cleaned, encoding="utf-8")
        return py_path, "ok"
    except Exception as e:
        return py_path, f"error: {e}"


def collect_files(input_dir: Path, suffix: str) -> list:
    pattern = f"*{suffix}.py" if suffix else "*.py"
    return sorted(input_dir.glob(pattern))


def main():
    parser = argparse.ArgumentParser(description="Postprocess CadQuery .py files")
    parser.add_argument("--input_dir", required=True, type=Path)
    parser.add_argument("--output_dir", type=Path, default=None)
    parser.add_argument("--suffix", type=str, default="")
    parser.add_argument("--inplace", action="store_true")
    parser.add_argument("--out_suffix", type=str, default="_clean")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--skip_existing", action="store_true")
    args = parser.parse_args()

    files = collect_files(args.input_dir, args.suffix)
    if not files:
        raise SystemExit(f"No files found in {args.input_dir} matching *{args.suffix}.py")
    print(f"Found {len(files)} files")

    tasks = []
    for f in files:
        if args.inplace:
            out = f
        elif args.output_dir:
            out = args.output_dir / f.name
        else:
            out = f.parent / f"{f.stem}{args.out_suffix}.py"

        if args.skip_existing and out.exists() and not args.inplace:
            continue
        tasks.append((f, out))

    print(f"Processing {len(tasks)} files with {args.workers} workers...")
    ok, errors = 0, []

    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(process_file, f, o): f for f, o in tasks}
        for i, fut in enumerate(as_completed(futures), 1):
            path, status = fut.result()
            if status == "ok":
                ok += 1
            else:
                errors.append((path, status))
            if i % 500 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)} done...")

    print(f"\nDone: {ok} ok, {len(errors)} errors")
    for p, e in errors[:20]:
        print(f"  {p.name}: {e}")


if __name__ == "__main__":
    main()
