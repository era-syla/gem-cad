# CAD Code Generation Pipeline

End-to-end pipeline for generating CadQuery code from CAD images using Gemini, converting to STEP, and building feature graphs.

---

## Scripts to Push

Push these scripts to run the pipeline on another device:

```
batch_gemini.py          # Send image batch jobs via Gemini File API
batch_images.py          # Alternative batch image script (inline requests)
convert_to_step.py       # Convert CadQuery .py files to .step
download_batch_results.py# Download results from completed Gemini batch jobs
make_vertex_jsonl.py     # Build JSONL for Vertex AI batch prediction jobs
postprocess_cq.py        # Clean up generated CadQuery files
iou.py                   # Compute normalized IOU between two STEP files
requirements.txt         # Python dependencies
```

From `fixing-samples` repo also push:
```
batch_stage1.py          # Stage 1: CadQuery → feature graph (via Gemini batch)
batch_stage2.py          # Stage 2: feature graph → CadQuery code (via Gemini batch)
prompts/graph_enrich_system.txt
prompts/code_gen_system.txt
```

---

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Also install Google Cloud CLI for Vertex AI jobs:
```bash
brew install --cask google-cloud-sdk
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

---

## Pipeline Overview

### 1. Generate CadQuery from Images (Gemini Batch API)

```bash
python batch_gemini.py \
  --input_dir /path/to/images \
  --output_dir /path/to/output \
  --suffix _31 \
  --thinking MEDIUM \
  --skip_existing \
  --workers 16 \
  --api_key $GEMINI_API_KEY
```

- Supports `--recursive` for subfolders (easy/medium/hard)
- Results saved as `{stem}_31.py` alongside images
- If interrupted, download results manually:

```bash
GEMINI_API_KEY=your_key python download_batch_results.py \
  --jobs BATCH_JOB_ID \
  --output_dir /path/to/output
```

---

### 2. Generate CadQuery via Vertex AI (for large batches: 10k–50k images)

**Step 1 — Upload images to GCS:**
```bash
gcloud storage cp "/path/to/images/**" gs://YOUR_BUCKET/images_batchN/ --no-clobber
```

**Step 2 — Generate JSONL prompt file** (edit `make_vertex_jsonl.py` to set `local_folder`, `bucket_uri`, `output_file`):
```bash
python make_vertex_jsonl.py
```

**Step 3 — Upload JSONL to GCS:**
```bash
gcloud storage cp prompts_batchN.jsonl gs://YOUR_BUCKET/
```

**Step 4 — Submit batch job** on Vertex AI console using the JSONL GCS path.

For a new batch folder, use this quick checklist:

1. Update `make_vertex_jsonl.py` with the new folder path and new output names, for example `images_batch3` and `prompts_batch3.jsonl`.
2. Upload images to GCS:

```bash
gcloud storage cp "/YOUR_FOLDER/**" gs://cadcode-batch-data-first/images_batch3/ --no-clobber
```

3. Generate and upload JSONL:

```bash
python make_vertex_jsonl.py
gcloud storage cp /Users/erasyla/gem-cad/prompts_batch3.jsonl gs://cadcode-batch-data-first/
```

Then submit on the Vertex AI console using `gs://cadcode-batch-data-first/prompts_batch3.jsonl`.

The JSONL format per line:
```json
{
  "request": {
    "contents": [{"role": "user", "parts": [
      {"text": "PROMPT"},
      {"fileData": {"mimeType": "image/png", "fileUri": "gs://bucket/images/file.png"}}
    ]}],
    "generationConfig": {"thinkingConfig": {"thinkingLevel": "MEDIUM"}}
  }
}
```

---

### 3. Convert CadQuery to STEP

```bash
python convert_to_step.py \
  --input_dir /path/to/py/files \
  --suffix _31 \
  --skip_existing \
  --workers 8 \
  --timeout 30
```

- Use `--suffix ""` if files have no suffix
- Failures logged to `convert_failures.tsv` in input dir
- Delete failed `.py` files before retry: check `convert_failures.tsv`

---

### 4. Postprocess CadQuery Files

Strips comments, `show_object()`, `exportStep()`, markdown fences, and fixes double-dot syntax errors:

```bash
python postprocess_cq.py \
  --input_dir /path/to/py/files \
  --suffix _31 \
  --inplace \
  --workers 8
```

---

### 5. Feature Graph Pipeline (2-stage)

**Stage 1 — CadQuery → Feature Graph:**
```bash
# Run in background (survives laptop close)
nohup caffeinate -i python /path/to/fixing-samples/batch_stage1.py \
  --input /path/to/cadquery/files \
  --apikey $GEMINI_API_KEY \
  --out graphs.jsonl > stage1_log.txt 2>&1 &
```

- Processes in chunks of 1000
- Resumes automatically from `graphs.jsonl` if interrupted

**Stage 2 — Feature Graph → CadQuery:**
```bash
nohup caffeinate -i python /path/to/fixing-samples/batch_stage2.py \
  --input graphs.jsonl \
  --apikey $GEMINI_API_KEY \
  --out /path/to/stage2_outputs > stage2_log.txt 2>&1 &
```

- Saves one `.py` file per graph in `--out` directory
- Resumes automatically if interrupted

---

## Tips

- Use `caffeinate -i` on Mac to prevent sleep during long jobs
- Always use `--skip_existing` on convert_to_step to avoid re-doing work
- Batch job IDs look like `batches/abc123...` — save them before closing terminal
- The Gemini model used: `gemini-3.1-pro-preview` with `MEDIUM` thinking
