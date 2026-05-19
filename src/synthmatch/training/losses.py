"""Loss skeletons for future inverse-synthesis training."""

from __future__ import annotations


def parameter_regression_loss(prediction: object, target: object) -> None:
    """Future supervised parameter loss."""

    _ = (prediction, target)
    raise NotImplementedError("TODO: implement after target vector encoding is finalized")

