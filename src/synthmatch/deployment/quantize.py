"""Quantization skeleton for future deployment."""

from __future__ import annotations


def quantize_for_inference(model_path: str, output_path: str) -> None:
    """Future quantization hook."""

    _ = (model_path, output_path)
    raise NotImplementedError("TODO: design quantization after deployment target is fixed")

