from synthmatch.synth.serial_protocol import SerialCommand, expected_num_samples, expected_pcm16_bytes


def test_expected_byte_count_calculation() -> None:
    assert expected_num_samples(1.0, 22050) == 22050
    assert expected_num_samples(2.0, 22050) == 44100
    assert expected_num_samples(4.0, 22050) == 88200
    assert expected_pcm16_bytes(22050) == 44100


def test_serial_protocol_command_definitions() -> None:
    assert SerialCommand.HELLO.value == "HELLO"
    assert SerialCommand.SET_PARAMS.value == "SET_PARAMS"
    assert SerialCommand.RENDER.value == "RENDER"
    assert SerialCommand.AUDIO_CHUNK.value == "AUDIO_CHUNK"
    assert SerialCommand.DONE.value == "DONE"
    assert SerialCommand.ERROR.value == "ERROR"

