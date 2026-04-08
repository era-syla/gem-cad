import os
import json

# Configuration
local_folder = "/Users/erasyla/gem-cad/second_batch_job_20k"
bucket_uri = "gs://cadcode-batch-data-first/images_batch2"
output_file = "prompts_batch2.jsonl"

prompt_text = """You are an expert CAD engineer and
3D modeling specialist with deep knowledge of
mechanical design, geometric modeling, and CadQuery.

Generate CadQuery Python code to create this 3D CAD model
based on the provided image.

Requirements:
- Use CadQuery syntax
- Create a variable called 'result' containing the final geometry
- Include all necessary imports
- Use parametric dimensions where appropriate
- The code must be executable and create valid solid geometry

Return ONLY the Python code, no explanations."""

count = 0
with open(output_file, 'w') as f:
    for filename in sorted(os.listdir(local_folder)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            ext = os.path.splitext(filename)[1].lower()
            mime_type = "image/png" if ext == ".png" else "image/jpeg"

            entry = {
                "request": {
                    "contents": [
                        {
                            "role": "user",
                            "parts": [
                                {"text": prompt_text},
                                {
                                    "fileData": {
                                        "mimeType": mime_type,
                                        "fileUri": f"{bucket_uri}/{filename}"
                                    }
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "thinkingConfig": {
                            "thinkingLevel": "MEDIUM"
                        }
                    }
                }
            }
            f.write(json.dumps(entry) + "\n")
            count += 1

print(f"Done! {output_file} created with {count} entries.")
