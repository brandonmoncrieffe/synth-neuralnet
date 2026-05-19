"""Minimal WAV IO helpers.

WAV files are the source of truth for generated examples. Feature extraction
should read WAVs rather than replacing them with precomputed spectrograms.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import wavfile


def save_pcm16_wav(path: str | Path, pcm: bytes | np.ndarray, sample_rate: int) -> None:
    """Save mono PCM16 audio to a WAV file."""

    wav_path = Path(path)
    wav_path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(pcm, bytes):
        audio = np.frombuffer(pcm, dtype="<i2")
    else:
        audio = np.asarray(pcm, dtype=np.int16)
    wavfile.write(wav_path, sample_rate, audio)


def load_wav(path: str | Path) -> tuple[int, np.ndarray]:
    """Load a WAV file as ``(sample_rate, samples)``."""

    return wavfile.read(Path(path))


def is_expected_audio_path(path: str | Path) -> bool:
    """Return whether a path follows the generated audio filename convention."""

    wav_path = Path(path)
    return wav_path.suffix == ".wav" and wav_path.stem.isdigit() and len(wav_path.stem) == 6

