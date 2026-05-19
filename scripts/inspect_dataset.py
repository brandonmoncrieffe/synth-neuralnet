#!/usr/bin/env python
"""Inspect a generated dataset manifest."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from synthmatch.data.dataset_manifest import load_manifest_entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to manifest.jsonl")
    args = parser.parse_args()

    entries = load_manifest_entries(args.manifest)
    print(f"entries: {len(entries)}")
    print(f"splits: {dict(Counter(entry.split for entry in entries))}")
    print(f"durations: {dict(Counter(entry.duration_seconds for entry in entries))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

