"""Audio metric skeletons for render comparison."""

from __future__ import annotations


def compare_audio(reference: object, candidate: object) -> None:
    """Future audio-distance metric hook."""

    _ = (reference, candidate)
    raise NotImplementedError("TODO: define audio metrics after baseline dataset exists")

