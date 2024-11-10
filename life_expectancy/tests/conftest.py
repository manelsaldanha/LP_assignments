"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR

@pytest.fixture(scope="session")
def eurostat_life_expect_raw() -> pd.DataFrame:
    """Fixture to load the raw json file"""
    return pd.read_json(FIXTURES_DIR / "eurostat_life_expect_raw.json")

@pytest.fixture(scope="session")
def eurostat_life_expect_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "eurostat_life_expect_expected.csv")

@pytest.fixture(scope="session")
def eu_life_expectancy_raw() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep='\t')

@pytest.fixture(scope="session")
def eu_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected.csv")
