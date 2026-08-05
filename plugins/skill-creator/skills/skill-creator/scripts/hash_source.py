#!/usr/bin/env python3
"""Print the canonical content hash for a frozen skill file or directory."""

import argparse
from pathlib import Path

try:
    from .aggregate_benchmark import sha256_source
except ImportError:
    from aggregate_benchmark import sha256_source


def main():
    parser = argparse.ArgumentParser(
        description="Hash a skill file or directory for protocol.json"
    )
    parser.add_argument("source", type=Path)
    args = parser.parse_args()

    if not args.source.exists():
        parser.error(f"source does not exist: {args.source}")
    print(sha256_source(args.source))


if __name__ == "__main__":
    main()
