"""Python-side serial protocol concepts for the ESP32-S3 synth.

This module defines command names and small validation helpers only. Firmware-
specific framing, checksums, and pyserial reads/writes are TODO.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SerialCommand(StrEnum):
    """Planned command and response concepts for the ESP32-S3 protocol."""

    HELLO = "HELLO"
    SET_PARAMS = "SET_PARAMS"
    RENDER = "RENDER"
    AUDIO_CHUNK = "AUDIO_CHUNK"
    DONE = "DONE"
    ERROR = "ERROR"


@dataclass(frozen=True)
class SerialConfig:
    """Serial connection settings for pyserial."""

    port: str | None
    baud_rate: int = 921600
    timeout_seconds: float = 5.0
    chunk_size_bytes: int = 4096
    dry_run: bool = True


def expected_num_samples(duration_seconds: float, sample_rate: int) -> int:
    """Return the expected mono sample count for a fixed-duration render."""

    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    return int(round(duration_seconds * sample_rate))


def expected_pcm16_bytes(num_samples: int, channels: int = 1) -> int:
    """Return byte count for signed 16-bit PCM audio."""

    if num_samples < 0:
        raise ValueError("num_samples must be non-negative")
    if channels <= 0:
        raise ValueError("channels must be positive")
    return num_samples * channels * 2


def checksum_placeholder(payload: bytes) -> int:
    """Placeholder checksum hook for the eventual firmware protocol."""

    # TODO: Replace with the checksum used by the ESP32-S3 firmware framing.
    return sum(payload) & 0xFFFF


def validate_audio_transfer_size(received_bytes: int, expected_bytes: int) -> None:
    """Validate that the received PCM payload has the expected byte count."""

    if received_bytes != expected_bytes:
        raise ValueError(f"Expected {expected_bytes} audio bytes, received {received_bytes}")

