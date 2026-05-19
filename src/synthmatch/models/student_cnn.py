"""Small future student model skeleton."""

from __future__ import annotations

try:
    import torch
    from torch import nn
except ImportError:  # pragma: no cover - dependency is declared in pyproject.
    torch = None
    nn = None


if nn is not None:

    class StudentCNN(nn.Module):
        """Placeholder for log-mel-spectrogram-to-parameter regression.

        This is intentionally not a detailed architecture. Define target vector
        encoding and baseline metrics before filling in model layers.
        """

        def __init__(self, num_targets: int) -> None:
            super().__init__()
            self.num_targets = num_targets

        def forward(self, features: "torch.Tensor") -> "torch.Tensor":
            raise NotImplementedError("TODO: implement minimal baseline architecture")

else:

    class StudentCNN:  # type: ignore[no-redef]
        """Import guard used when torch is not installed."""

        def __init__(self, num_targets: int) -> None:
            _ = num_targets
            raise ImportError("torch is required to instantiate StudentCNN")

