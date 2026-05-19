from scripts.generate_clean_dataset import generate_duration_schedule, generate_split_schedule


def test_duration_bucket_schedule_counts() -> None:
    schedule = generate_duration_schedule(
        10,
        [
            {"duration_seconds": 1.0, "proportion": 0.70},
            {"duration_seconds": 2.0, "proportion": 0.20},
            {"duration_seconds": 4.0, "proportion": 0.10},
        ],
        seed=1234,
    )

    assert schedule.count(1.0) == 7
    assert schedule.count(2.0) == 2
    assert schedule.count(4.0) == 1


def test_split_schedule_counts() -> None:
    schedule = generate_split_schedule(10, 0.8, 0.1, 0.1, seed=1234)

    assert schedule.count("train") == 8
    assert schedule.count("val") == 1
    assert schedule.count("test") == 1

