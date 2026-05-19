from pathlib import Path

from synthmatch.synth.param_sampler import ParamSampler


def test_param_sampler_is_deterministic() -> None:
    path = Path("configs/params_schema.yaml")
    first = ParamSampler.from_yaml(path, seed=123).sample()
    second = ParamSampler.from_yaml(path, seed=123).sample()

    assert first == second


def test_param_sampler_outputs_schema_valid_params() -> None:
    sampler = ParamSampler.from_yaml(Path("configs/params_schema.yaml"), seed=123)
    params = sampler.sample()

    sampler.schema.validate_params(params)

