"""Renderer abstractions for hardware and future software comparison paths."""

from __future__ import annotations

from typing import Protocol


class RendererInterface(Protocol):
    """Protocol implemented by hardware or future simulator renderers."""

    def render_pcm16(self, params: dict[str, object], duration_seconds: float, sample_rate: int) -> bytes:
        """Render raw PCM16 bytes for a parameter dictionary."""

