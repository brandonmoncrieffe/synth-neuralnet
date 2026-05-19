"""Output head skeletons for synth parameter prediction."""

from __future__ import annotations


class ParameterHead:
    """Placeholder for mixed continuous/categorical parameter heads."""

    def encode_targets(self, params: dict[str, object]) -> None:
        """Encode parameter dictionaries as training targets."""

        _ = params
        raise NotImplementedError("TODO: implement target vector encoding from real schema")

