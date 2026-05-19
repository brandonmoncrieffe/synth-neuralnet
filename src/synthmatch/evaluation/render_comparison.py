"""Utilities for future render comparisons."""

from __future__ import annotations


def render_and_compare(params: dict[str, object], target_audio_path: str) -> None:
    """Future helper for comparing synth render with a target WAV."""

    _ = (params, target_audio_path)
    raise NotImplementedError("TODO: implement once hardware render path is available")

