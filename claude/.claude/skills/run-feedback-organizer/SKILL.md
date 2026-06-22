---
name: run-feedback-organizer
description: Organize images into sets for feedback tool. Interview about your pipeline (inputs, image processing, preprocessing), generate and run a custom script, save numbered sets (set1/, set2/, etc.) with mapping CSV.
---

Interactive tool to organize images into numbered sets for the feedback comparison tool.

## Overview

This skill interviews you about your specific image organization pipeline, generates a custom script tailored to your needs, runs it, and produces a feedback-ready directory structure with a mapping CSV.

## Run (Agent Path)

**Interview workflow** — I will ask you clarifying questions about your pipeline:

1. **Input sources** — What folders/files/CSVs contain your images?
2. **Image processing per position** — How to generate each image position:
   - Position 1: Copy from folder? Apply transformation?
   - Position 2: Composite/blend? Different version?
   - Position 3: Another variant?
3. **Common preprocessing** — What to apply to all images after position-specific processing?
4. **Output location and metadata** — Where to save? What mapping to keep?

Once you answer, I will:
- **Generate** a Python script from `template.py`, filling in your specific pipeline
- **Save** it as `feedback_job.py` in the current directory
- **Run** it on your images
- **Show** the output directory and mapping file

## Output Structure

```
feedback_sets/
├── set1/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
├── set2/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
...
└── mapping.csv
```

**mapping.csv format:**
```
set_number,original_image_name
set1,image_001
set2,image_002
```

## Prerequisites

```bash
pip install Pillow
```

## How to Fill the Template

I will customize `template.py` by filling in three key functions:

1. **`get_input_data()`** — Load your input data
   - Return a list of dicts, one per output set
   - Each dict should contain identifiers/metadata for that set
   - Examples: `[{'filename': 'image_001'}, ...]` or load from CSV

2. **`process_image_for_position(item, position)`** — Generate each image
   - Called for each position (1, 2, 3, ...) for each set
   - Return a PIL Image in RGB mode, or None if this position shouldn't exist
   - Handle different transformations per position

3. **`apply_common_preprocessing(image)`** — Preprocess all images
   - Applied after position-specific processing
   - Examples: JPEG compression (handled at save time), resize, etc.
   - Can return image unchanged if no preprocessing needed

**See EXAMPLES.md for real-world implementations** of these functions.

## Gotchas

- **Flexibility** — Your inputs can be anything (folders, CSVs, mixed). `get_input_data()` is where you customize this.
- **PIL Image modes** — Always convert to RGB before returning from `process_image_for_position()`. The infrastructure handles the rest.
- **Compositing** — Use PIL's `Image.paste(im, box, mask)` for efficient image layering with transparency.
- **File naming** — The mapping file captures your original image names — make sure `get_input_data()` includes a `'name'` or `'filename'` key per item.

## Troubleshooting

**"NotImplementedError: Fill in get_input_data()"**
- I didn't fully understand your input source. Clarify which folders/files have your images.

**Output has wrong number of images per set**
- Check `process_image_for_position()` — it should return None to stop creating images, or continue returning images for more positions.

**Composite images look wrong**
- Verify masks are RGBA or grayscale (L mode), not RGB. If RGB, convert with `.convert('L')` first.
- Check background colors (RGB tuples like `(255, 0, 0)` for red).

**File sizes too large**
- Add preprocessing: resize in `apply_common_preprocessing()` or reduce JPEG quality at save time.

**Missing common files**
- If some images exist in only some folders, `get_input_data()` needs to filter to only the common ones. Use set intersection: `common = set1 & set2 & set3`
