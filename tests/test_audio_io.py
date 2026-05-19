from synthmatch.data.audio_io import is_expected_audio_path


def test_audio_path_convention() -> None:
    assert is_expected_audio_path("data/raw/clean_mixed_10k/audio/000001.wav")
    assert not is_expected_audio_path("data/raw/clean_mixed_10k/audio/example.wav")
    assert not is_expected_audio_path("data/raw/clean_mixed_10k/audio/000001.flac")

