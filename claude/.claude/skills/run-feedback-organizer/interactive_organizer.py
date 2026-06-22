#!/usr/bin/env python3
"""
Interactive organizer for feedback tool image sets.

This is called by the Claude agent to:
1. Ask clarifying questions about your pipeline
2. Generate a filled-in script
3. Run the script
"""

import sys
import subprocess
from pathlib import Path
import json

def ask_user_for_pipeline_details():
    """
    Ask the user to describe their image organization pipeline.

    Returns a dict with pipeline configuration that can be used to
    fill in the template.
    """
    print("\n" + "="*70)
    print("FEEDBACK IMAGE ORGANIZER - INTERACTIVE SETUP")
    print("="*70)
    print()
    print("I'll ask you about your specific image organization needs.")
    print("Based on your answers, I'll generate a custom script.")
    print()

    # This will be filled in by the Claude agent asking the user
    # For now, this is a placeholder that the agent will use
    raise NotImplementedError(
        "This script is called by Claude agent with AskUserQuestion. "
        "The agent will collect user answers and generate the final script."
    )

def generate_script_from_template(
    template_path: Path,
    user_answers: dict,
    output_script_path: Path
):
    """
    Fill in the template with user's answers to generate the final script.

    Args:
        template_path: Path to template.py
        user_answers: Dict with user's pipeline configuration
        output_script_path: Where to save the generated script
    """
    with open(template_path) as f:
        template = f.read()

    # TODO: Fill in the template based on user_answers
    # For now, this is a placeholder

    with open(output_script_path, 'w') as f:
        f.write(template)

    print(f"Generated script: {output_script_path}")

def run_script(script_path: Path, output_dir: Path):
    """Run the generated script."""
    result = subprocess.run(
        ['python3', str(script_path), str(output_dir)],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr, file=sys.stderr)

    return result.returncode == 0

if __name__ == '__main__':
    print("This script is designed to be called by Claude agent with AskUserQuestion.")
    print("It provides the template and infrastructure for generating custom scripts.")
    print()
    print("Template location:", Path(__file__).parent / 'template.py')
