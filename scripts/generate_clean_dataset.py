#!/usr/bin/env python
"""Generate clean paired parameter/audio examples from the ESP32-S3 synth.

This script defaults to dry-run mode and does not fabricate audio. Real dataset
generation requires the firmware-specific serial protocol implementation.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from synthmatch.data.dataset_manifest import manifest_contains_example
from synthmatch.synth.param_sampler import ParamSampler
from synthmatch.synth.serial_protocol import SerialConfig, expected_num_samples, expected_pcm16_bytes
from synthmatch.synth.synth_controller import SynthController


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/dataset_clean_mixed_10k.yaml", help="Dataset YAML config path.")
    parser.add_argument("--serial-port", default=None, help="Override serial port from config.")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Force dry-run mode.")
    parser.add_argument("--no-dry-run", action="store_true", help="Disable dry-run mode and require hardware.")
    parser.add_argument("--resume", action="store_true", help="Force resume behavior on.")
    parser.add_argument("--no-resume", action="store_true", help="Force resume behavior off.")
    return parser.parse_args()


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def generate_duration_schedule(
    num_examples: int,
    duration_buckets: list[dict[str, float]],
    seed: int,
) -> list[float]:
    """Create a deterministic shuffled duration schedule from bucket proportions."""

    if num_examples < 0:
        raise ValueError("num_examples must be non-negative")
    proportions = [float(bucket["proportion"]) for bucket in duration_buckets]
    if abs(sum(proportions) - 1.0) > 1e-6:
        raise ValueError("duration bucket proportions must sum to 1.0")

    counts = [int(num_examples * proportion) for proportion in proportions]
    while sum(counts) < num_examples:
        remainders = [
            (num_examples * proportions[index]) - counts[index]
            for index in range(len(duration_buckets))
        ]
        counts[remainders.index(max(remainders))] += 1

    schedule: list[float] = []
    for bucket, count in zip(duration_buckets, counts, strict=True):
        schedule.extend([float(bucket["duration_seconds"])] * count)

    rng = random.Random(seed)
    rng.shuffle(schedule)
    return schedule


def generate_split_schedule(num_examples: int, train: float, val: float, test: float, seed: int) -> list[str]:
    """Create a deterministic shuffled split schedule."""

    if abs((train + val + test) - 1.0) > 1e-6:
        raise ValueError("train/val/test splits must sum to 1.0")
    train_count = int(num_examples * train)
    val_count = int(num_examples * val)
    test_count = num_examples - train_count - val_count
    splits = ["train"] * train_count + ["val"] * val_count + ["test"] * test_count
    rng = random.Random(seed + 1)
    rng.shuffle(splits)
    return splits


def example_paths(output_dir: Path, example_id: str) -> tuple[Path, Path]:
    return output_dir / "audio" / f"{example_id}.wav", output_dir / "params" / f"{example_id}.json"


def is_example_complete(output_dir: Path, manifest_path: Path, example_id: str) -> bool:
    """Return whether audio, params, and manifest row already exist."""

    audio_path, params_path = example_paths(output_dir, example_id)
    return audio_path.exists() and params_path.exists() and manifest_contains_example(manifest_path, example_id)


def main() -> int:
    args = parse_args()
    config = load_config(args.config)

    dry_run = bool(config.get("dry_run", {}).get("enabled", True))
    if args.dry_run:
        dry_run = True
    if args.no_dry_run:
        dry_run = False

    resume = bool(config.get("resume", {}).get("enabled", True))
    if args.resume:
        resume = True
    if args.no_resume:
        resume = False

    output_dir = PROJECT_ROOT / config["output_dir"]
    audio_dir = output_dir / "audio"
    params_dir = output_dir / "params"
    manifest_path = output_dir / "manifest.jsonl"
    audio_dir.mkdir(parents=True, exist_ok=True)
    params_dir.mkdir(parents=True, exist_ok=True)

    schema_path = PROJECT_ROOT / "configs" / "params_schema.yaml"
    sampler = ParamSampler.from_yaml(schema_path, seed=int(config["seed"]))

    serial_cfg = config["serial"]
    serial_port = args.serial_port if args.serial_port is not None else serial_cfg.get("port")
    controller = SynthController(
        SerialConfig(
            port=serial_port,
            baud_rate=int(serial_cfg["baud_rate"]),
            timeout_seconds=float(serial_cfg["timeout_seconds"]),
            chunk_size_bytes=int(serial_cfg["chunk_size_bytes"]),
            dry_run=dry_run,
        )
    )

    num_examples = int(config["num_examples"])
    if dry_run:
        num_examples = min(num_examples, int(config.get("dry_run", {}).get("max_examples", 10)))

    durations = generate_duration_schedule(num_examples, config["duration_buckets"], int(config["seed"]))
    splits = generate_split_schedule(
        num_examples,
        float(config["train_split"]),
        float(config["val_split"]),
        float(config["test_split"]),
        int(config["seed"]),
    )

    controller.connect()
    controller.hello()

    try:
        for index, (duration_seconds, split) in enumerate(zip(durations, splits, strict=True)):
            example_id = f"{index:06d}"
            audio_path, params_path = example_paths(output_dir, example_id)
            if resume and is_example_complete(output_dir, manifest_path, example_id):
                print(f"skip complete example {example_id}")
                continue

            params = sampler.sample()
            num_samples = expected_num_samples(duration_seconds, int(config["sample_rate"]))
            expected_bytes = expected_pcm16_bytes(num_samples, channels=int(config["channels"]))

            if dry_run:
                planned = {
                    "example_id": example_id,
                    "duration_seconds": duration_seconds,
                    "split": split,
                    "audio_path": str(audio_path.relative_to(output_dir)),
                    "params_path": str(params_path.relative_to(output_dir)),
                    "num_samples": num_samples,
                    "expected_bytes": expected_bytes,
                    "dry_run": True,
                }
                print(json.dumps(planned, sort_keys=True))
                continue

            # TODO: Capture timing around send/render/receive once protocol exists.
            pcm = controller.render_or_capture(params, duration_seconds, int(config["sample_rate"]), audio_path)
            _ = pcm
            # TODO: save WAV, save params JSON, and append ManifestEntry with real timings.
            raise NotImplementedError("Real dataset generation awaits ESP32 serial protocol implementation")
    finally:
        controller.disconnect()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
