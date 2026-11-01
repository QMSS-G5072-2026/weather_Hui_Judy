import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import weather_jyh2142


def test_version_is_defined():
    assert isinstance(weather_jyh2142.__version__, str)


@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32),
        (100, 212),
        (-40, -40),
        (37, 98.6),
        (-273.15, -459.67),
    ],
)
def test_celsius_to_fahrenheit(celsius, expected):
    actual = weather_jyh2142.celsius_to_fahrenheit(celsius)
    assert actual == pytest.approx(expected)


@pytest.mark.parametrize(
    "bad_input, expected_error",
    [
        ("12", TypeError),
        (None, TypeError),
        (-273.16, ValueError),
        (-1212.12, ValueError),
    ],
)
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    with pytest.raises(expected_error):
        weather_jyh2142.celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    temps = [10.0, float("nan"), 20.0]
    actual = weather_jyh2142.summarize_temperatures(temps)

    assert actual["mean"] == pytest.approx(15.0)
    assert actual["min"] == pytest.approx(10.0)
    assert actual["max"] == pytest.approx(20.0)
    assert actual["n_missing"] == 1


@pytest.fixture
def raw_readings():
    return pd.DataFrame(
        {
            "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
            "date": [
                "2026-07-02",
                "2026-07-01",
                "2026-07-01",
                "2026-07-02",
                "2026-07-01",
            ],
            "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
        }
    )


def test_raw_readings_fixture(raw_readings):
    assert list(raw_readings) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert sum(pd.isna(raw_readings["temp_c"])) == 1


def test_clean_readings(raw_readings):
    expected = pd.DataFrame(
        {
            "station": ["CPK", "JFK", "LGA"],
            "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
            "temp_c": [25.0, 30.0, 28.0],
            "temp_f": [77.0, 86.0, 82.4],
        }
    )

    actual = weather_jyh2142.clean_readings(raw_readings)

    assert_frame_equal(actual, expected)
