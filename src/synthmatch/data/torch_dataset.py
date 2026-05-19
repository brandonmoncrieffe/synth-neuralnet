"""PyTorch dataset skeleton for paired WAV/parameter examples."""

from __future__ import annotations

from pathlib import Path

from synthmatch.data.dataset_manifest import ManifestEntry, load_manifest_entries


class SynthMatchDataset:
    """Dataset wrapper around manifest rows.

    TODO: Subclass ``torch.utils.data.Dataset`` once feature extraction and
    target vector encoding are defined.
    """

    def __init__(self, manifest_path: str | Path) -> None:
        self.manifest_path = Path(manifest_path)
        self.entries: list[ManifestEntry] = load_manifest_entries(self.manifest_path)

    def __len__(self) -> int:
        return len(self.entries)

    def __getitem__(self, index: int) -> ManifestEntry:
        return self.entries[index]

