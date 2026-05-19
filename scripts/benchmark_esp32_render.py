#!/usr/bin/env python
"""Benchmark ESP32-S3 render and transfer timings.

Skeleton only. Dry-run mode prints planned measurements without contacting
hardware or fabricating performance results.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from synthmatch.synth.serial_protocol import expected_num_samples, expected_pcm16_bytes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-rate", type=int, default=22050)
    parser.add_argument("--durations", type=float, nargs="+", default=[1.0, 2.0, 4.0])
    parser.add_argument("--serial-port", default=None)
    parser.add_argument("--baud-rate", type=int, default=921600)
    parser.add_argument("--dry-run", action="store_true", default=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for duration_seconds in args.durations:
        num_samples = expected_num_samples(duration_seconds, args.sample_rate)
        expected_bytes = expected_pcm16_bytes(num_samples)
        row = {
            "sample_rate": args.sample_rate,
            "duration_seconds": duration_seconds,
            "num_samples": num_samples,
            "expected_bytes": expected_bytes,
            "render_time_us": None,
            "transfer_time_us": None,
            "total_time_us": None,
            "realtime_factor": None,
            "bytes_received": None,
            "effective_kb_per_second": None,
            "serial_port": args.serial_port,
            "baud_rate": args.baud_rate,
            "dry_run": True,
        }
        print(json.dumps(row, sort_keys=True))

    # TODO: Add render-only and render+transfer protocol calls after firmware framing is final.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

