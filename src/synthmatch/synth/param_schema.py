"""Parameter schema loading and validation helpers.

The schema in ``configs/params_schema.yaml`` is intentionally a placeholder.
Replace it with the fixed ESP32-S3 parameter set before collecting real data.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml

ParameterType = Literal["float", "int", "bool", "categorical"]


@dataclass(frozen=True)
class ParameterSpec:
    """Single synthesizer parameter definition."""

    name: str
    type: ParameterType
    default: Any
    min: float | int | None = None
    max: float | int | None = None
    allowed_values: tuple[Any, ...] | None = None
    sampling_strategy: str = "uniform"
    include_in_target: bool = True
    placeholder: bool = False


@dataclass(frozen=True)
class ParameterSchema:
    """Loaded synthesizer parameter schema."""

    schema_version: str
    parameters: tuple[ParameterSpec, ...]

    @property
    def names(self) -> tuple[str, ...]:
        """Return parameter names in schema order."""

        return tuple(spec.name for spec in self.parameters)

    @property
    def target_names(self) -> tuple[str, ...]:
        """Return parameter names included in the ML target vector."""

        return tuple(spec.name for spec in self.parameters if spec.include_in_target)

    def validate_params(self, params: dict[str, Any]) -> None:
        """Validate a sampled or loaded parameter dictionary."""

        expected = set(self.names)
        actual = set(params)
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            raise ValueError(f"Parameter keys do not match schema. missing={missing}, extra={extra}")

        for spec in self.parameters:
            value = params[spec.name]
            _validate_value(spec, value)


def load_parameter_schema(path: str | Path) -> ParameterSchema:
    """Load a parameter schema from YAML."""

    schema_path = Path(path)
    with schema_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    if not isinstance(raw, dict):
        raise ValueError(f"Expected mapping at top level of {schema_path}")

    raw_parameters = raw.get("parameters")
    if not isinstance(raw_parameters, list) or not raw_parameters:
        raise ValueError("Parameter schema must contain a non-empty 'parameters' list")

    specs = tuple(_parse_parameter_spec(item) for item in raw_parameters)
    schema = ParameterSchema(
        schema_version=str(raw.get("schema_version", "unknown")),
        parameters=specs,
    )
    _validate_unique_names(schema)
    for spec in schema.parameters:
        _validate_default(spec)
    return schema


def _parse_parameter_spec(raw: dict[str, Any]) -> ParameterSpec:
    if not isinstance(raw, dict):
        raise ValueError("Each parameter spec must be a mapping")

    name = raw.get("name")
    param_type = raw.get("type")
    if not isinstance(name, str) or not name:
        raise ValueError("Parameter spec is missing a non-empty name")
    if param_type not in {"float", "int", "bool", "categorical"}:
        raise ValueError(f"Unsupported parameter type for {name}: {param_type}")

    allowed_values = raw.get("allowed_values")
    return ParameterSpec(
        name=name,
        type=param_type,
        default=raw.get("default"),
        min=raw.get("min"),
        max=raw.get("max"),
        allowed_values=tuple(allowed_values) if allowed_values is not None else None,
        sampling_strategy=str(raw.get("sampling_strategy", "uniform")),
        include_in_target=bool(raw.get("include_in_target", True)),
        placeholder=bool(raw.get("placeholder", False)),
    )


def _validate_unique_names(schema: ParameterSchema) -> None:
    names = schema.names
    if len(set(names)) != len(names):
        raise ValueError("Parameter names must be unique")


def _validate_default(spec: ParameterSpec) -> None:
    _validate_value(spec, spec.default)


def _validate_value(spec: ParameterSpec, value: Any) -> None:
    if spec.type == "bool":
        if not isinstance(value, bool):
            raise ValueError(f"{spec.name} must be a bool")
        return

    if spec.type == "categorical":
        if not spec.allowed_values:
            raise ValueError(f"{spec.name} must define allowed_values")
        if value not in spec.allowed_values:
            raise ValueError(f"{spec.name}={value!r} is not in allowed_values")
        return

    if spec.type == "int":
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{spec.name} must be an int")
    elif spec.type == "float":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{spec.name} must be numeric")

    if spec.min is None or spec.max is None:
        raise ValueError(f"{spec.name} must define min and max")
    if value < spec.min or value > spec.max:
        raise ValueError(f"{spec.name}={value!r} is outside [{spec.min}, {spec.max}]")

