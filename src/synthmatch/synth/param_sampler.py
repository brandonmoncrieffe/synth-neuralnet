"""Deterministic parameter sampling for ESP32-S3 dataset generation."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any

from synthmatch.synth.param_schema import ParameterSchema, ParameterSpec, load_parameter_schema


class ParamSampler:
    """Sample valid parameter dictionaries from a fixed synth schema.

    Advanced musical priors, correlated parameters, and coverage-aware sampling
    are intentionally left for later. This class only guarantees deterministic,
    schema-valid samples.
    """

    def __init__(self, schema: ParameterSchema, seed: int | None = None) -> None:
        self.schema = schema
        self._rng = random.Random(seed)

    @classmethod
    def from_yaml(cls, path: str | Path, seed: int | None = None) -> "ParamSampler":
        """Create a sampler from a YAML schema path."""

        return cls(load_parameter_schema(path), seed=seed)

    def sample(self) -> dict[str, Any]:
        """Sample one schema-valid parameter dictionary."""

        params = {spec.name: self._sample_spec(spec) for spec in self.schema.parameters}
        self.schema.validate_params(params)
        return params

    def _sample_spec(self, spec: ParameterSpec) -> Any:
        if spec.sampling_strategy not in {"uniform", "log_uniform_todo"}:
            # TODO: Add named sampling strategies after real parameter ranges are known.
            return spec.default

        if spec.type == "categorical":
            if not spec.allowed_values:
                raise ValueError(f"{spec.name} has no allowed_values")
            return self._rng.choice(spec.allowed_values)

        if spec.type == "bool":
            return bool(self._rng.getrandbits(1))

        if spec.min is None or spec.max is None:
            raise ValueError(f"{spec.name} must define min and max")

        if spec.type == "int":
            return self._rng.randint(int(spec.min), int(spec.max))

        if spec.type == "float":
            return self._rng.uniform(float(spec.min), float(spec.max))

        raise ValueError(f"Unsupported parameter type: {spec.type}")

