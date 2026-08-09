#!/usr/bin/env python3
"""
Quick validation script for Skill Forge skills.

This is a fast SKILL.md sanity check. It intentionally accepts the Claude Code
plugin frontmatter fields used by this repository, but it does not replace
`claude plugin validate` or `make validate`.
"""

import argparse
import sys
import re
import yaml
from pathlib import Path

def validate_skill(skill_path, max_description_chars=1024):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties. Keep this aligned with the frontmatter used by
    # Skill Forge's Claude Code plugin skills.
    ALLOWED_PROPERTIES = {
        'name',
        'description',
        'license',
        'allowed-tools',
        'metadata',
        'compatibility',
        'disable-model-invocation',
        'argument-hint',
    }

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if not description:
        return False, "Description must not be empty"
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > max_description_chars:
            return False, (
                f"Description is too long ({len(description)} characters). "
                f"Maximum is {max_description_chars} characters."
            )

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    allowed_tools = frontmatter.get('allowed-tools')
    if allowed_tools is not None:
        if not isinstance(allowed_tools, list) or not all(isinstance(item, str) for item in allowed_tools):
            return False, "'allowed-tools' must be a YAML list of strings"

    disable_model_invocation = frontmatter.get('disable-model-invocation')
    if disable_model_invocation is not None and not isinstance(disable_model_invocation, bool):
        return False, "'disable-model-invocation' must be a boolean"

    argument_hint = frontmatter.get('argument-hint')
    if argument_hint is not None:
        valid_hint = isinstance(argument_hint, str) or (
            isinstance(argument_hint, list)
            and all(isinstance(item, str) for item in argument_hint)
        )
        if not valid_hint:
            return False, "'argument-hint' must be a string or YAML list of strings"

    return True, "Skill is valid!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a skill directory")
    parser.add_argument("skill_directory")
    parser.add_argument(
        "--max-description-chars",
        type=int,
        default=1024,
        help="Description budget for the target repository (default: format limit 1024)",
    )
    args = parser.parse_args()
    if not 1 <= args.max_description_chars <= 1024:
        parser.error("--max-description-chars must be between 1 and 1024")

    valid, message = validate_skill(
        args.skill_directory,
        max_description_chars=args.max_description_chars,
    )
    print(message)
    sys.exit(0 if valid else 1)
