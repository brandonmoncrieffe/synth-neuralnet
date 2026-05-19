"""High-level controller interface for rendering audio from the ESP32-S3 synth."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from synthmatch.synth.serial_protocol import SerialConfig, expected_num_samples


class SynthController:
    """Coordinate parameter upload, rendering, and raw PCM capture.

    Hardware communication is intentionally not implemented yet. The final
    implementation should use pyserial, chunked binary reads, timeout handling,
    expected byte count validation, and firmware-specific checksums/framing.
    """

    def __init__(self, config: SerialConfig) -> None:
        self.config = config
        self.is_connected = False

    def connect(self) -> None:
        """Open the serial connection."""

        if self.config.dry_run:
            self.is_connected = True
            return
        if self.config.port is None:
            raise ValueError("A serial port is required when dry_run=False")
        raise NotImplementedError("TODO: open pyserial connection to ESP32-S3")

    def disconnect(self) -> None:
        """Close the serial connection."""

        if self.config.dry_run:
            self.is_connected = False
            return
        raise NotImplementedError("TODO: close pyserial connection")

    def hello(self) -> bool:
        """Verify that the firmware is responding."""

        if self.config.dry_run:
            return True
        raise NotImplementedError("TODO: send HELLO and parse firmware response")

    def send_params(self, params: dict[str, Any]) -> None:
        """Send one complete parameter set to the ESP32-S3 synth."""

        if self.config.dry_run:
            return
        raise NotImplementedError("TODO: encode and send SET_PARAMS payload")

    def render(self, duration_seconds: float, sample_rate: int) -> None:
        """Request a fixed-duration render from the ESP32-S3."""

        if self.config.dry_run:
            return
        raise NotImplementedError("TODO: send RENDER command with sample count")

    def receive_audio(self, expected_num_samples: int) -> bytes:
        """Receive raw PCM16 audio bytes from the ESP32-S3."""

        if self.config.dry_run:
            raise NotImplementedError("Dry-run mode does not fabricate audio bytes")
        raise NotImplementedError("TODO: receive AUDIO_CHUNK messages until DONE")

    def render_or_capture(
        self,
        params: dict[str, Any],
        duration_seconds: float,
        sample_rate: int,
        output_path: str | Path,
    ) -> bytes:
        """Send params, render audio, receive PCM, and leave WAV writing to caller."""

        self.send_params(params)
        self.render(duration_seconds=duration_seconds, sample_rate=sample_rate)
        num_samples = expected_num_samples(duration_seconds, sample_rate)
        pcm = self.receive_audio(num_samples)
        # TODO: The caller will write ``pcm`` to ``output_path`` once real capture exists.
        _ = Path(output_path)
        return pcm

