"""
Upload local .py + .png pairs to DeCoDELab/gemcad_data in the same
parquet format as the existing dataset (sample_id, code, image columns).

Expects a flat directory where each sample has matching filenames:
  my_sample.py
  my_sample.png

New shards are appended — existing data in the repo is untouched.

Run with:
  python upload_to_gemcad.py --token YOUR_TOKEN --input-dir /path/to/your/files
"""
import argparse
import json
from io import BytesIO
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from PIL import Image
from huggingface_hub import HfApi

DST_REPO   = "DeCoDELab/gemcad_data"
CKPT_FILE  = Path("upload_ckpt.json")
SHARD_SIZE = 1000

IMAGE_TYPE = pa.struct([
    pa.field("bytes", pa.large_binary()),
    pa.field("path",  pa.large_string()),
])
SCHEMA = pa.schema([
    pa.field("sample_id", pa.large_string()),
    pa.field("code",      pa.large_string()),
    pa.field("image",     IMAGE_TYPE),
])


def load_ckpt():
    if CKPT_FILE.exists():
        with open(CKPT_FILE) as f:
            d = json.load(f)
        return set(d["done"]), d["num_shards"]
    return set(), 0


def save_ckpt(done: set, num_shards: int):
    with open(CKPT_FILE, "w") as f:
        json.dump({"done": list(done), "num_shards": num_shards}, f)


def build_parquet(rows):
    """rows: list of (sample_id, code_str, image_bytes). Returns BytesIO."""
    table = pa.table({
        "sample_id": pa.array([r[0] for r in rows], type=pa.large_string()),
        "code":      pa.array([r[1] for r in rows], type=pa.large_string()),
        "image":     pa.array(
            [{"bytes": r[2], "path": None} for r in rows],
            type=IMAGE_TYPE,
        ),
    }, schema=SCHEMA)
    buf = BytesIO()
    pq.write_table(table, buf, compression="snappy")
    buf.seek(0)
    return buf


def get_next_shard_index(api):
    """Find the highest existing shard index in the repo to avoid overwriting."""
    try:
        existing = list(api.list_repo_files(repo_id=DST_REPO, repo_type="dataset"))
        indices = []
        for f in existing:
            if f.startswith("data/train-") and f.endswith(".parquet"):
                try:
                    indices.append(int(f.split("train-")[1].split(".")[0]))
                except ValueError:
                    pass
        return max(indices) + 1 if indices else 0
    except Exception:
        return 0


def chunked(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token",      required=True, help="HF token with write access")
    parser.add_argument("--input-dir",  required=True, help="Directory containing .py + .png pairs")
    parser.add_argument("--shard-size", type=int, default=SHARD_SIZE)
    parser.add_argument("--image-ext",  default="png", help="Image extension (default: png)")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        raise SystemExit(f"Directory not found: {input_dir}")

    api = HfApi(token=args.token)

    # ── Find paired files ─────────────────────────────────────────────────────
    py_files  = {p.stem: p for p in input_dir.glob("*.py")}
    # Renders are saved as {stem}_0.png — strip the trailing _0 to match py stem
    img_files = {}
    for p in input_dir.glob(f"*.{args.image_ext}"):
        stem = p.stem
        if stem.endswith("_0"):
            stem = stem[:-2]
        img_files[stem] = p
    paired    = sorted(set(py_files) & set(img_files))

    if not paired:
        raise SystemExit(f"No matched .py + .{args.image_ext} pairs found in {input_dir}")
    print(f"Found {len(paired):,} paired samples in {input_dir}")

    # ── Resume ────────────────────────────────────────────────────────────────
    done_ids, _ = load_ckpt()
    todo = [sid for sid in paired if sid not in done_ids]
    print(f"  {len(done_ids):,} already uploaded, {len(todo):,} remaining")

    # Start shard index after whatever already exists in the repo
    shard_num = get_next_shard_index(api)
    print(f"  Next shard index in repo: {shard_num}\n")

    # ── Upload shards ─────────────────────────────────────────────────────────
    total_errors = []

    for chunk in chunked(todo, args.shard_size):
        rows   = []
        errors = []

        for sid in chunk:
            try:
                code = py_files[sid].read_text(encoding="utf-8", errors="replace")
                img = Image.open(img_files[sid])
                if img.mode != "RGB":
                    img = img.convert("RGB")
                buf = BytesIO()
                img.save(buf, format="PNG")
                image_bytes = buf.getvalue()
                rows.append((sid, code, image_bytes))
            except Exception as e:
                errors.append((sid, str(e)))
                print(f"  READ ERROR {sid}: {e}")

        if rows:
            parquet_buf = build_parquet(rows)
            shard_name  = f"data/train-{shard_num:05d}.parquet"
            api.upload_file(
                path_or_fileobj=parquet_buf,
                path_in_repo=shard_name,
                repo_id=DST_REPO,
                repo_type="dataset",
                commit_message=f"Add shard {shard_num} ({len(rows)} samples)",
            )
            for sid, _, _ in rows:
                done_ids.add(sid)
            save_ckpt(done_ids, shard_num + 1)
            shard_num += 1

        total_errors.extend(errors)
        print(f"  Shard {shard_num}: {len(rows)} pushed, {len(errors)} errors  "
              f"| total uploaded: {len(done_ids):,}/{len(paired):,}")

    save_ckpt(done_ids, shard_num)
    print(f"\nDone. {len(done_ids):,}/{len(paired):,} samples added to {DST_REPO}")
    if total_errors:
        print(f"  {len(total_errors)} failed — re-run to retry (checkpoint saved)")


if __name__ == "__main__":
    main()
