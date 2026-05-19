"""Checkpoint helpers for future training runs."""

from __future__ import annotations


def save_checkpoint(path: str, state: dict[str, object]) -> None:
    """Future checkpoint save hook."""

    _ = (path, state)
    raise NotImplementedError("TODO: implement once training state is defined")

