# Example Pipelines

These are examples of how to fill in the template for common scenarios.

## Example 1: Input + Mask Overlays

**Scenario:** You have an `input/` folder with images and a `masks/` folder with corresponding mask files. You want to create:
- Position 1: Original input image
- Position 2: Input with mask overlaid using red background
- Position 3: Input with mask overlaid using blue background

**Template fills:**

```python
def get_input_data():
    from pathlib import Path
    items = []
    for img in Path('input').glob('*.jpg'):
        items.append({'filename': img.stem})
    return items

def process_image_for_position(item, position):
    from pathlib import Path
    from PIL import Image
    
    filename = item['filename']
    
    if position == 1:
        # Original input
        return Image.open(f'input/{filename}.jpg').convert('RGB')
    
    elif position == 2:
        # Input with mask on red background
        base = Image.open(f'input/{filename}.jpg').convert('RGB')
        mask = Image.open(f'masks/{filename}.png')
        
        # Create red background and composite mask onto it
        red_bg = Image.new('RGB', base.size, (255, 0, 0))
        
        if mask.mode == 'RGBA':
            # Extract alpha channel for transparency
            mask_rgb = mask.convert('RGB')
            alpha = mask.split()[3]
            red_bg.paste(mask_rgb, (0, 0), alpha)
        elif mask.mode == 'L':
            # Grayscale mask
            red_bg.paste(mask.convert('RGB'), (0, 0), mask)
        
        # Now blend with input using mask alpha
        if mask.mode == 'RGBA':
            alpha = mask.split()[3]
        else:
            alpha = mask.convert('L')
        
        # Create result by blending base and red_bg
        result = Image.new('RGB', base.size)
        result.paste(base, (0, 0))
        result.paste(red_bg, (0, 0), alpha)
        
        return result
    
    elif position == 3:
        # Input with mask on blue background (same approach, different color)
        base = Image.open(f'input/{filename}.jpg').convert('RGB')
        mask = Image.open(f'masks/{filename}.png')
        
        blue_bg = Image.new('RGB', base.size, (0, 0, 255))
        
        if mask.mode == 'RGBA':
            mask_rgb = mask.convert('RGB')
            alpha = mask.split()[3]
            blue_bg.paste(mask_rgb, (0, 0), alpha)
        elif mask.mode == 'L':
            blue_bg.paste(mask.convert('RGB'), (0, 0), mask)
        
        if mask.mode == 'RGBA':
            alpha = mask.split()[3]
        else:
            alpha = mask.convert('L')
        
        result = Image.new('RGB', base.size)
        result.paste(base, (0, 0))
        result.paste(blue_bg, (0, 0), alpha)
        
        return result
    
    return None

def apply_common_preprocessing(image):
    # No additional preprocessing; quality applied at save time
    return image
```

Run: `python feedback_job.py ./feedback_sets`

---

## Example 2: Multiple Processing Versions from CSV

**Scenario:** You have a CSV file with image names and scores. You want to organize them sorted by score, with:
- Position 1: Original image
- Position 2: Processed version (grayscale)
- Position 3: Processed version (edge detection)

**Template fills:**

```python
import csv
from pathlib import Path
from PIL import Image
import numpy as np

def get_input_data():
    items = []
    with open('results.csv') as f:
        reader = csv.DictReader(f)
        for row in sorted(reader, key=lambda x: float(x['score']), reverse=True):
            items.append({
                'filename': row['image_name'],
                'score': float(row['score'])
            })
    return items

def process_image_for_position(item, position):
    filename = item['filename']
    
    if position == 1:
        return Image.open(f'images/{filename}').convert('RGB')
    
    elif position == 2:
        # Grayscale version
        img = Image.open(f'images/{filename}').convert('RGB')
        gray = img.convert('L')
        return Image.merge('RGB', (gray, gray, gray))
    
    elif position == 3:
        # Edge detection
        img = Image.open(f'images/{filename}').convert('RGB')
        img_array = np.array(img)
        
        # Simple edge detection
        edges = np.sqrt(
            np.gradient(img_array, axis=0)**2 + 
            np.gradient(img_array, axis=1)**2
        )
        edges = (edges / edges.max() * 255).astype(np.uint8)
        
        return Image.fromarray(edges).convert('RGB')
    
    return None

def apply_common_preprocessing(image):
    # Resize to 50%
    return image.resize(
        (image.width // 2, image.height // 2),
        Image.Resampling.LANCZOS
    )
```

---

## Example 3: Folder-by-folder comparison

**Scenario:** You have multiple result folders (e.g., `method_a/`, `method_b/`, `method_c/`) with the same image names. You want each set to show:
- Position 1: Result from method_a
- Position 2: Result from method_b  
- Position 3: Result from method_c

**Template fills:**

```python
from pathlib import Path

def get_input_data():
    items = []
    base_path = Path('method_a')
    
    for img_file in sorted(base_path.glob('*.jpg')):
        items.append({'filename': img_file.stem})
    
    return items

def process_image_for_position(item, position):
    methods = ['method_a', 'method_b', 'method_c']
    
    if position > len(methods):
        return None
    
    method = methods[position - 1]
    filename = item['filename']
    
    img_path = Path(method) / f"{filename}.jpg"
    if img_path.exists():
        return Image.open(img_path).convert('RGB')
    
    return None

def apply_common_preprocessing(image):
    # 70% JPEG quality (will be applied at save time)
    return image
```

---

## Tips for Custom Pipelines

1. **Finding common files:** Use `sorted(Path(folder).glob(...))` and set intersections to find matching names
2. **Handling different formats:** Use `img.convert('RGB')` before saving
3. **CSV sorting:** Use `sorted(csv.DictReader(...), key=lambda x: x['field'])`
4. **Image compositing:** Use PIL's `Image.paste(im, box, mask)` — it's efficient and handles alpha blending
5. **Heavy preprocessing:** Do it in `apply_common_preprocessing()` so all images get the same treatment
