# Read version from installed package
from importlib.metadata import version

from weather_jyh2142.weather_jyh2142 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)

__version__ = version("weather_jyh2142")

__all__ = [
    "__version__",
    "celsius_to_fahrenheit",
    "clean_readings",
    "summarize_temperatures",
]
