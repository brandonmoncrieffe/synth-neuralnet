from pathlib import Path

from synthmatch.synth.param_schema import load_parameter_schema


def test_load_placeholder_parameter_schema() -> None:
    schema = load_parameter_schema(Path("configs/params_schema.yaml"))

    assert "osc_waveform" in schema.names
    assert "filter_cutoff" in schema.names
    assert all(spec.placeholder for spec in schema.parameters)
    assert schema.target_names == schema.names

