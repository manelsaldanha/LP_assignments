"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR

@pytest.fixture(scope="session")
def eurostat_life_expect_raw() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_json(FIXTURES_DIR / "eurostat_life_expect_raw.json")

@pytest.fixture(scope="session")
def eurostat_life_expect_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "eurostat_life_expect_expected.csv")
