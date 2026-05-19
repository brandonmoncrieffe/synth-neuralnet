"""Audio capture boundary for future ESP32-S3 raw PCM streaming."""

from __future__ import annotations


class AudioCapture:
    """Placeholder for chunked PCM capture over serial."""

    def read_pcm16(self, expected_bytes: int) -> bytes:
        """Read exactly ``expected_bytes`` from the serial stream."""

        raise NotImplementedError("TODO: implement chunked binary PCM reads from pyserial")

