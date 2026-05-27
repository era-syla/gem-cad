# CAD Augmentation Pipeline

## Overview

```
Original Image (.png)
        │
        ▼
   [batch_gemini.py]          image → CadQuery Python
        │
        ▼
  Original CadQuery (.py)
        │
        ▼
   [batch_stage1.py]          CadQuery → enriched feature graph (JSON)
        │
        ▼
  Feature Graph (.jsonl)
        │
        ▼
   [batch_stage2.py]          feature graph → new CadQuery Python
        │
        ▼
  Augmented CadQuery (.py)
        │
        ▼
  [convert_to_step.py]        execute + BRepCheck validation → STEP
        │
        ▼
  Valid STEP file (.step)
```

---

## Stage 0 — Image → CadQuery (`batch_gemini.py`)

- Input: grayscale rendered PNG of a CAD part
- Model: Gemini (vision) reads the image and writes CadQuery Python that reconstructs the shape
- Output: `.py` file with a `result` variable holding the CadQuery solid
- Failures are skipped; valid files move to Stage 1

---

## Stage 1 — CadQuery → Feature Graph (`batch_stage1.py`)

**Prompt:** `graph_enrich_system.txt`

- Parses the CadQuery code into a structured JSON array of nodes
- Each node has: `id`, `type`, `operation`, `produces`, and geometry params
- **Enrichment:** adds 5–8 new nodes (holes, fillets, ribs, patterns, etc.)
- Node types: `Feature`, `Boolean`, `Modifier`, `Sketch`, `Pattern`
- Dependencies always point to lower ids (no forward references)

Example enriched graph:
```json
[
  {"id":1,"type":"Feature","operation":"box","length":80,"width":40,"height":15,"produces":"base"},
  {"id":2,"type":"Modifier","operation":"fillet","radius":2,"inputs":[1],"produces":"base_filleted","note":"NEW: soften edges"},
  {"id":3,"type":"Feature","operation":"cylinder","radius":3,"length":20,"produces":"hole_tool","note":"NEW: M6 hole"},
  {"id":4,"type":"Boolean","operation":"cut","target":2,"tool":3,"produces":"result","note":"NEW: cut hole"}
]
```

---

## Stage 2 — Feature Graph → CadQuery (`batch_stage2.py`)

**Prompt:** `code_gen_system.txt`

- Takes the enriched feature graph and generates fresh CadQuery Python
- Processes nodes in ascending id order
- Each node's `produces` field becomes the Python variable name
- Final solid must be assigned to `result`
- Diversity rules: varies base planes, construction methods, fillet/chamfer styles

---

## Validation (`convert_to_step.py`)

- Executes each `.py` file in a subprocess
- Runs `BRepCheck_Analyzer` on the resulting shape
- Exports to `.step` only if valid
- Failures logged to `convert_failures.tsv`

Current validity rates:
- Original CadQuery (Stage 0): ~95%+
- Stage 2 outputs (before fix): ~59%
- Stage 2 outputs (after LLM fix): TBD

---

## Fixing Failures (`batch_fix_errors.py` + `prefix_cq.py`)

1. **Programmatic pre-fix** (`prefix_cq.py`): removes hallucinated methods (`filterBy`, `StringSelector`, `polarArray`), fixes invalid plane names, ensures `result` variable exists
2. **LLM fix** (`batch_fix_errors.py`): sends failed file + error message to Gemini, gets corrected code back

---

## Why Fillets/Chamfers Are Over-Represented

Stage 1 adds fillets/chamfers to nearly every graph because the enrichment prompt lists them as the first suggested modifier. This creates a bias in Stage 2 outputs. Fix: make Stage 1 add fillets only ~30% of the time and use other modifiers otherwise.
