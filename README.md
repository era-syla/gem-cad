# GemCAD Pipeline

End-to-end pipeline for generating CadQuery code from CAD images using Gemini, converting to STEP, and evaluating with IOU scoring.

---

## Installation

```bash
pip install google-genai cadquery pythonocc-core openai anthropic pyarrow pillow huggingface-hub
```

Or install the minimal set for batch generation only:
```bash
pip install -r requirements.txt
```

---

## Scripts

### Generation

#### `batch_gemini.py`
Batch Gemini API caller for CAD model generation from single-view images.

```bash
GEMINI_API_KEY=your_key python batch_gemini.py \
  --input_dir ./images \
  --output_dir ./results \
  --skip_existing \
  --workers 8
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--input_dir` | required | Directory containing input images |
| `--output_dir` | `./results` | Directory for output `.py` files |
| `--model` | `gemini-3.1-pro-preview` | Gemini model name |
| `--suffix` | `_31` | Suffix for output `.py` files |
| `--thinking` | None | Thinking level: `LOW`, `MEDIUM`, `HIGH` |
| `--workers` | `8` | Parallel upload workers |
| `--skip_existing` | False | Skip images that already have output |
| `--max_images` | None | Limit number of images |
| `--recursive` | False | Recurse into subfolders |
| `--poll_interval` | `30` | Seconds between batch status polls |

---

#### `batch_gemini_multiview.py`
Same as `batch_gemini.py` but prompts the model to treat the input as 4 views of one shape. Default suffix is `_31_mv`.

```bash
GEMINI_API_KEY=your_key python batch_gemini_multiview.py \
  --input_dir ./multiview_images \
  --output_dir ./results_mv \
  --skip_existing \
  --workers 8
```

---

#### `single_gemini.py`
Single (non-batch) Gemini API calls — useful for quick testing or small sets.

```bash
GEMINI_API_KEY=your_key python single_gemini.py \
  --input_dir ./images \
  --max_images 10 \
  --thinking MEDIUM \
  --rpm 30
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--thinking` | None | `LOW`, `MEDIUM`, `HIGH`, `OFF` |
| `--thinking_budget` | None | Max thinking tokens |
| `--rpm` | `60` | Max requests per minute |
| `--files` | None | Comma-separated specific filenames |

---

#### `batch_images.py`
Alternative batch caller using inline image data instead of File API uploads.

```bash
GEMINI_API_KEY=your_key python batch_images.py \
  --input_dir ./images \
  --output_dir ./results \
  --workers 8
```

---

#### `make_vertex_jsonl.py`
Builds a JSONL request file for Vertex AI batch prediction jobs. Edit `local_folder`, `bucket_uri`, and `output_file` in the script before running.

```bash
python make_vertex_jsonl.py
```

---

### Post-processing

#### `postprocess_cq.py`
Cleans raw Gemini outputs: strips markdown fences, removes `#` comments, removes `show_object()` and `.exportStep()` calls, fixes double-dot syntax errors.

```bash
python postprocess_cq.py \
  --input_dir ./results \
  --suffix _31 \
  --inplace
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--inplace` | False | Modify files in place |
| `--out_suffix` | `_clean` | Suffix for output files if not inplace |
| `--workers` | `8` | Parallel workers |

---

### Fixing Invalid Samples

#### `fix_invalid.py`
Fixes scripts that failed execution or geometry validation by re-prompting Gemini with the error and a catalogue of common CadQuery failure modes.

```bash
python fix_invalid.py \
  --input_dir ./results \
  --output_dir ./valid_cq \
  --workers 4
```

---

#### `fix_cq_errors.py`
Fixes failing CadQuery scripts using OpenAI or Gemini with the error message as context.

```bash
python fix_cq_errors.py \
  --input_dir ./results \
  --provider gemini \
  --api_key YOUR_KEY \
  --workers 4
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--provider` | `openai` | `openai` or `gemini` |
| `--thinking` | None | Gemini thinking level |
| `--max_fixes` | None | Limit number of scripts to fix |

---

#### `batch_fix_chunks.py`
Batch version of the fix pipeline — reads a TSV of failures and submits them as a Gemini batch job.

```bash
python batch_fix_chunks.py \
  --tsv /tmp/failures.tsv \
  --api_key YOUR_KEY \
  --chunk_name chunk1 \
  --py_dir ./results
```

---

### Conversion & Validation

#### `convert_to_step.py`
Converts CadQuery `.py` files to STEP and validates geometry with OpenCASCADE `BRepCheck_Analyzer`.

```bash
python convert_to_step.py \
  --input_dir ./results \
  --suffix _31 \
  --workers 8
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--output_dir` | `{input_dir}_step/` | Where to save STEP files |
| `--timeout` | `30` | Max seconds per conversion |
| `--skip_existing` | False | Skip already converted files |

---

#### `json_to_step.py`
Converts `generated` CadQuery code from prediction JSON files to STEP files. Expects JSON with `file_id` and `generated` fields.

```bash
python json_to_step.py \
  --input predictions.json \
  --output_dir ./step_outputs \
  --workers 8 \
  --timeout 30
```

---

#### `validate_and_collect.py`
Converts CadQuery files to STEP, validates geometry, and collects valid pairs into an output folder.

```bash
python validate_and_collect.py \
  --output_dir ./valid_cq \
  --workers 8
```

---

### IOU Scoring

#### `iou.py`
Core IOU utility. Loads two STEP files, aligns them via center of mass and principal axes of inertia, and computes volumetric IOU.

```bash
python iou.py ground_truth.step generated.step
```

---

#### `batch_iou.py`
Computes IOU scores across a directory of generated STEP files vs ground truth.

```bash
python batch_iou.py \
  --input_dir ./gt_steps \
  --gen_dir ./generated_steps \
  --suffix _31 \
  --output scores.json \
  --workers 8
```

---

#### `batch_iou_orcd.py`
IOU scoring for ORCD — matches `{file_id}.step` (GT) with `{file_id}_gen.step` (predicted). Outputs per-sample scores and summary stats including valid rate, mean, and median IOU.

```bash
python batch_iou_orcd.py \
  --gt_dir /path/to/gt_steps \
  --pred_dir /path/to/pred_steps \
  --output results.json \
  --workers 8 \
  --timeout 120
```

---

### Batch Management

#### `download_batch_results.py`
Downloads results from completed Gemini batch jobs.

```bash
GEMINI_API_KEY=your_key python download_batch_results.py \
  --jobs JOB_ID1 JOB_ID2 \
  --output_dir ./results \
  --suffix _31
```

---

#### `check_batch_status.py`
Checks the status of a submitted Gemini batch job and optionally polls until completion.

```bash
python check_batch_status.py \
  --batch batches/abc123 \
  --apikey YOUR_KEY \
  --poll \
  --out results.jsonl
```

---

### Dataset Upload

#### `upload_to_gemcad.py`
Uploads `.py` + `.png` pairs to the `DeCoDELab/gemcad_data` HuggingFace dataset in parquet format with resumable checkpointing.

```bash
python upload_to_gemcad.py \
  --token YOUR_HF_TOKEN \
  --input-dir /path/to/valid_cq \
  --shard-size 500
```

---

## Dependencies

| Package | Used by |
|---------|---------|
| `google-genai` | All `batch_gemini*` scripts |
| `cadquery` | `convert_to_step`, `fix_invalid`, `validate_and_collect`, `json_to_step` |
| `pythonocc-core` | `iou.py`, `batch_iou*.py` |
| `openai` | `fix_cq_errors` (OpenAI provider) |
| `anthropic` | `fix_invalid` |
| `pyarrow` | `upload_to_gemcad` |
| `pillow` | `upload_to_gemcad` |
| `huggingface-hub` | `upload_to_gemcad` |
