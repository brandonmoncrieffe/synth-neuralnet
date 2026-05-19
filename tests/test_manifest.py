from synthmatch.data.dataset_manifest import ManifestEntry, validate_manifest_entry_paths


def test_manifest_entry_json_roundtrip() -> None:
    entry = ManifestEntry(
        example_id="000001",
        audio_path="audio/000001.wav",
        params_path="params/000001.json",
        sample_rate=22050,
        duration_seconds=1.0,
        num_samples=22050,
        audio_format="pcm16",
        channels=1,
        synth_version="esp32_s3_v0",
        generation_seed=1234,
        split="train",
        serial_port=None,
        baud_rate=921600,
        render_time_us=None,
        transfer_time_us=None,
        total_time_us=None,
        bytes_received=None,
        effective_kb_per_second=None,
        realtime_factor=None,
    )

    restored = ManifestEntry.from_json_line(entry.to_json_line())
    assert restored == entry
    validate_manifest_entry_paths(entry, "data/raw/clean_mixed_10k")

