"""Manifest structures for paired synth parameter/audio examples."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

Split = Literal["train", "val", "test"]


@dataclass(frozen=True)
class ManifestEntry:
    """One dataset manifest row."""

    example_id: str
    audio_path: str
    params_path: str
    sample_rate: int
    duration_seconds: float
    num_samples: int
    audio_format: str
    channels: int
    synth_version: str
    generation_seed: int
    split: Split
    serial_port: str | None
    baud_rate: int
    render_time_us: int | None
    transfer_time_us: int | None
    total_time_us: int | None
    bytes_received: int | None
    effective_kb_per_second: float | None
    realtime_factor: float | None

    def to_json_line(self) -> str:
        """Serialize the entry as one JSONL row."""

        return json.dumps(asdict(self), sort_keys=True)

    @classmethod
    def from_json_line(cls, line: str) -> "ManifestEntry":
        """Deserialize one JSONL row."""

        return cls(**json.loads(line))


def append_manifest_entry(path: str | Path, entry: ManifestEntry) -> None:
    """Append a manifest row.

    TODO: Add atomic append or periodic manifest rebuild once generation is active.
    """

    manifest_path = Path(path)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as handle:
        handle.write(entry.to_json_line())
        handle.write("\n")


def load_manifest_entries(path: str | Path) -> list[ManifestEntry]:
    """Load manifest entries from JSONL. Missing manifests return an empty list."""

    manifest_path = Path(path)
    if not manifest_path.exists():
        return []
    with manifest_path.open("r", encoding="utf-8") as handle:
        return [ManifestEntry.from_json_line(line) for line in handle if line.strip()]


def manifest_contains_example(path: str | Path, example_id: str) -> bool:
    """Return whether a manifest contains an example id."""

    return any(entry.example_id == example_id for entry in load_manifest_entries(path))


def validate_manifest_entry_paths(entry: ManifestEntry, dataset_root: str | Path) -> None:
    """Validate path conventions for one manifest entry.

    TODO: Add expected sample count, sample rate, split, and parameter JSON checks.
    """

    root = Path(dataset_root)
    audio_path = root / entry.audio_path
    params_path = root / entry.params_path
    if audio_path.suffix != ".wav":
        raise ValueError(f"audio_path must point to a WAV file: {entry.audio_path}")
    if params_path.suffix != ".json":
        raise ValueError(f"params_path must point to a JSON file: {entry.params_path}")

