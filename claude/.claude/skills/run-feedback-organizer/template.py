#!/usr/bin/env python3
"""
Template script for organizing images into feedback tool sets.

Each project fills in these functions based on their specific needs:
- get_input_data()
- process_image_for_position()
- apply_common_preprocessing()

The rest of the infrastructure (set creation, mapping generation, etc.) is provided.
"""

from pathlib import Path
from PIL import Image
import csv
import logging
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# FILL IN THESE FUNCTIONS FOR YOUR SPECIFIC PIPELINE
# ============================================================================

def get_input_data() -> List[Dict[str, Any]]:
    """
    Load and prepare input data.

    This should return a list of dicts, one per output set. Each dict should
    contain any information needed to identify and process that set's images.

    Examples:
    - Return list of dicts with 'folder' and 'id' keys
    - Return list loaded from CSV with image names and metadata
    - Return list built by scanning folders and matching files

    Returns:
        List[Dict]: Each dict represents one set to create
    """
    # TODO: Fill this in
    # Example:
    # return [
    #     {'filename': 'image_001'},
    #     {'filename': 'image_002'},
    # ]
    raise NotImplementedError("Fill in get_input_data() for your specific inputs")

def process_image_for_position(item: Dict[str, Any], position: int) -> Image.Image:
    """
    Process an image for a specific position (1.jpg, 2.jpg, 3.jpg, etc.).

    This function is called once per position for each set.

    Args:
        item: One dict from get_input_data()
        position: Image position (1, 2, 3, ...)

    Returns:
        PIL Image: The processed image in RGB mode

    Examples:
    - Position 1: return input image from folder
    - Position 2: composite mask on top of input with red background
    - Position 3: return grayscale version
    - Return None if this position shouldn't exist for this set
    """
    # TODO: Fill this in
    # Example:
    # if position == 1:
    #     return Image.open(f'input/{item["filename"]}.jpg').convert('RGB')
    # elif position == 2:
    #     base = Image.open(f'input/{item["filename"]}.jpg').convert('RGB')
    #     mask = Image.open(f'masks/{item["filename"]}.png')
    #     # ... composite logic here
    #     return composite_image
    # return None
    raise NotImplementedError("Fill in process_image_for_position() for your specific processing")

def apply_common_preprocessing(image: Image.Image) -> Image.Image:
    """
    Apply preprocessing that should be applied to ALL images.

    This runs after position-specific processing.

    Args:
        image: PIL Image in RGB mode

    Returns:
        PIL Image: Preprocessed image

    Examples:
    - Apply JPEG compression by saving with specific quality
    - Resize image
    - Adjust color/contrast
    - Return unchanged if no preprocessing needed
    """
    # TODO: Fill this in
    # Example to reduce file size:
    # return image.resize((image.width // 2, image.height // 2), Image.Resampling.LANCZOS)
    return image

# ============================================================================
# INFRASTRUCTURE (Don't modify unless you know what you're doing)
# ============================================================================

def save_image(image: Image.Image, output_path: Path, format: str = 'jpg', **kwargs):
    """Save image with optional parameters (e.g., quality for JPEG)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format == 'jpg':
        image.save(output_path, 'JPEG', quality=kwargs.get('quality', 90), optimize=True)
    else:
        image.save(output_path, format.upper())

def find_max_positions(items: List[Dict[str, Any]]) -> int:
    """Determine how many image positions each set should have."""
    max_pos = 0
    for item in items:
        pos = 1
        while process_image_for_position(item, pos) is not None:
            max_pos = max(max_pos, pos)
            pos += 1
            if pos > 10:  # Safety limit
                break
    return max_pos

def organize_images(output_dir: Path, format: str = 'jpg', format_kwargs: Dict = None):
    """Main function to create sets and mapping."""
    output_dir.mkdir(parents=True, exist_ok=True)
    format_kwargs = format_kwargs or {}

    logger.info("Loading input data...")
    items = get_input_data()
    logger.info(f"Found {len(items)} items to process")

    max_positions = find_max_positions(items)
    logger.info(f"Each set will have up to {max_positions} images")

    mapping = []

    for set_num, item in enumerate(items, 1):
        set_dir = output_dir / f"set{set_num}"
        set_dir.mkdir(exist_ok=True)

        original_name = item.get('name', item.get('filename', f'item_{set_num}'))

        for position in range(1, max_positions + 1):
            try:
                image = process_image_for_position(item, position)
                if image is None:
                    continue

                # Ensure RGB
                image = image.convert('RGB')

                # Apply common preprocessing
                image = apply_common_preprocessing(image)

                # Save
                ext = '.jpg' if format == 'jpg' else f'.{format}'
                output_path = set_dir / f"{position}{ext}"
                save_image(image, output_path, format=format, **format_kwargs)

            except Exception as e:
                logger.warning(f"Failed to process set{set_num} position {position}: {e}")
                continue

        mapping.append({'set_number': f'set{set_num}', 'original_image_name': original_name})
        logger.info(f"Created set{set_num}")

    # Save mapping CSV
    mapping_file = output_dir / 'mapping.csv'
    with open(mapping_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['set_number', 'original_image_name'])
        writer.writeheader()
        writer.writerows(mapping)

    logger.info(f"Saved mapping to {mapping_file}")
    logger.info(f"Created {len(items)} sets in {output_dir}")

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        output_dir = Path(sys.argv[1])
    else:
        output_dir = Path('./feedback_sets')

    organize_images(output_dir)
    print(f"\n✓ Done! Output at: {output_dir}")
