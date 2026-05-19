"""Feature extraction skeletons for future training.

WAV remains the source of truth. Log-mel spectrograms and normalization should
be computed during training or explicit preprocessing experiments.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StftConfig:
    """Future STFT/log-mel configuration."""

    sample_rate: int = 22050
    n_fft: int = 1024
    hop_length: int = 256
    n_mels: int = 80


def load_waveform_for_features(path: str) -> None:
    """Future waveform loading hook."""

    raise NotImplementedError("TODO: load waveform and return tensor for feature extraction")


def compute_log_mel_spectrogram(waveform: object, config: StftConfig) -> None:
    """Future log-mel extraction hook."""

    _ = (waveform, config)
    raise NotImplementedError("TODO: implement log-mel extraction for training")

