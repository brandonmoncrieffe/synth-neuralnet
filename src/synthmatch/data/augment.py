"""Audio augmentation skeletons.

MEMS mic adaptation and domain augmentation come later, after clean direct
digital data is working.
"""

from __future__ import annotations


def apply_training_augmentations(waveform: object) -> object:
    """Return waveform unchanged until augmentation policy is designed."""

    # TODO: Add carefully scoped augmentation after baseline training works.
    return waveform

