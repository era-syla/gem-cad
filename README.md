# GemCAD Pipeline

End-to-end pipeline for generating CadQuery code from CAD images using Gemini, converting to STEP, and evaluating with IOU scoring.

---

## Installation

```bash
pip install google-genai cadquery pythonocc-core openai anthropic pyarrow pillow huggingface-hub
```

---

## Scripts

### 1. `generate.py`
Generate CadQuery code from CAD images using Gemini. Supports batch (via Gemini Batch API) and single (direct API) modes. Use `--multiview` for images containing 4 views of the same object.

```bash
# Batch mode (default) — upload, submit, poll, download
GEMINI_API_KEY=key python generate.py \
  --input_dir ./images \
  --output_dir ./results \
  --skip_existing \
  --workers 8

# Multi-view images (4 views per image)
GEMINI_API_KEY=key python generate.py \
  --input_dir ./multiview_images \
  --output_dir ./results \
  --multiview

# Single mode — direct API calls, useful for testing
GEMINI_API_KEY=key python generate.py \
  --input_dir ./images \
  --output_dir ./results \
  --mode single \
  --max_images 10 \
  --thinking MEDIUM
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--input_dir` | required | Directory containing input images |
| `--output_dir` | `./results` | Directory for output `.py` files |
| `--mode` | `batch` | `batch` or `single` |
| `--multiview` | False | Use 4-view prompt |
| `--model` | `gemini-3.1-pro-preview` | Gemini model |
| `--suffix` | `_31` (`_31_mv` if multiview) | Output file suffix |
| `--thinking` | None | `LOW`, `MEDIUM`, `HIGH` |
| `--workers` | `8` | Parallel upload workers |
| `--skip_existing` | False | Skip already-processed images |
| `--max_images` | None | Limit number of images |
| `--recursive` | False | Recurse into subfolders |
| `--rpm` | `60` | Max requests/min (single mode) |

---

### 2. `postprocess_cq.py`
Clean raw Gemini outputs: strip markdown fences, remove `#` comments, remove `show_object()` and `.exportStep()` calls, fix double-dot syntax errors.

```bash
python postprocess_cq.py \
  --input_dir ./results \
  --suffix _31 \
  --inplace
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--inplace` | False | Modify files in place |
| `--out_suffix` | `_clean` | Suffix for output if not inplace |
| `--workers` | `8` | Parallel workers |

---

### 3. `fix_cadquery.py`
Fix failing CadQuery scripts using Gemini (batch or single) or OpenAI. Reads a TSV of failures (`filename\terror`), re-prompts the model with error context, saves fixed scripts.

```bash
# Gemini batch (recommended for large sets)
python fix_cadquery.py \
  --tsv failures.tsv \
  --input_dir ./results \
  --provider gemini \
  --mode batch

# OpenAI single
python fix_cadquery.py \
  --tsv failures.tsv \
  --input_dir ./results \
  --provider openai \
  --mode single \
  --workers 4
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--tsv` | required | TSV file with `filename\terror` |
| `--provider` | `gemini` | `gemini` or `openai` |
| `--mode` | `batch` | `batch` or `single` |
| `--thinking` | None | Gemini thinking level |
| `--workers` | `4` | Parallel workers (single mode) |
| `--max_fixes` | None | Limit number to fix |

---

### 4. `fix_invalid.py`
Fix scripts that failed execution or BRepCheck validation by re-prompting Gemini with the error and a catalogue of common CadQuery failure modes. Can fully rewrite from scratch.

```bash
python fix_invalid.py \
  --input_dir ./results \
  --output_dir ./valid_cq \
  --workers 4
```

---

### 5. `py_to_step.py`
Convert CadQuery `.py` files to STEP. Supports directory input or JSON predictions file. Optionally validates geometry with OpenCASCADE `BRepCheck_Analyzer`.

```bash
# From directory
python py_to_step.py \
  --input_dir ./results \
  --suffix _31 \
  --validate \
  --workers 8

# From JSON predictions file
python py_to_step.py \
  --input_json predictions.json \
  --output_dir ./step_outputs \
  --workers 8
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--input_dir` | — | Directory with `.py` files |
| `--input_json` | — | JSON file with `file_id` + `generated` |
| `--output_dir` | `{input_dir}_step/` | Where to save STEP files |
| `--validate` | False | Run BRepCheck topology validation |
| `--timeout` | `30` | Max seconds per conversion |
| `--failures_tsv` | None | Write failed conversions to TSV |

---

### 6. `compute_iou.py`
Compute volumetric IOU between ground truth and generated STEP files. Supports same-directory (suffix-based matching) or separate GT/pred directories.

```bash
# Same directory (GT + generated in same dir)
python compute_iou.py \
  --input_dir ./bench0_steps \
  --suffix _31 \
  --output scores.json

# Separate GT and predicted directories
python compute_iou.py \
  --gt_dir ./gt_steps \
  --pred_dir ./pred_steps \
  --output scores.json \
  --workers 8 \
  --timeout 120
```

Output JSON includes `valid_rate`, `mean_iou`, `median_iou`, per-sample scores, and error details.

---

### 7. `manage_batches.py`
Check status of Gemini batch jobs, poll until completion, and download results.

```bash
# List all jobs
python manage_batches.py --list

# Check and download a specific job
python manage_batches.py \
  --check batches/abc123 \
  --poll \
  --download \
  --output_dir ./results

# Multiple jobs
python manage_batches.py \
  --check batches/abc123 batches/def456 \
  --download \
  --output_dir ./results
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--check` | — | Job ID(s) to check |
| `--list` | False | List all batch jobs |
| `--poll` | False | Poll until terminal state |
| `--download` | False | Download results if succeeded |
| `--output_format` | `py` | `py` or `jsonl` |
| `--interval` | `30` | Poll interval in seconds |

---

### 8. `upload_to_gemcad.py`
Upload `.py` + `.png` pairs to the `DeCoDELab/gemcad_data` HuggingFace dataset in parquet format with resumable checkpointing.

```bash
python upload_to_gemcad.py \
  --token YOUR_HF_TOKEN \
  --input-dir /path/to/valid_cq \
  --shard-size 500
```

---

### 9. `iou.py`
Core IOU library. Loads STEP files, aligns shapes via center of mass and principal axes of inertia, computes volumetric IOU. Used as a module by `compute_iou.py`.

```bash
# Direct usage
python iou.py ground_truth.step generated.step
```

---

## Typical Workflow

```bash
# 1. Generate CadQuery code from images
GEMINI_API_KEY=key python generate.py --input_dir ./images --output_dir ./results --skip_existing

# 2. Clean outputs
python postprocess_cq.py --input_dir ./results --suffix _31 --inplace

# 3. Convert to STEP (validates geometry)
python py_to_step.py --input_dir ./results --suffix _31 --validate --failures_tsv failures.tsv

# 4. Fix failed scripts
python fix_cadquery.py --tsv failures.tsv --input_dir ./results --provider gemini --mode batch

# 5. Compute IOU against ground truth
python compute_iou.py --gt_dir ./gt_steps --pred_dir ./results_step --output scores.json

# 6. Upload to HuggingFace
python upload_to_gemcad.py --token HF_TOKEN --input-dir ./results
```

---

## Dependencies

| Package | Used by |
|---------|---------|
| `google-genai` | `generate.py`, `fix_cadquery.py`, `manage_batches.py` |
| `cadquery` | `py_to_step.py`, `fix_invalid.py` |
| `pythonocc-core` | `iou.py`, `compute_iou.py`, `py_to_step.py` |
| `openai` | `fix_cadquery.py` (OpenAI provider) |
| `anthropic` | `fix_invalid.py` |
| `pyarrow` | `upload_to_gemcad.py` |
| `pillow` | `upload_to_gemcad.py` |
| `huggingface-hub` | `upload_to_gemcad.py` |
