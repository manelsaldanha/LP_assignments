"""Tests for the cleaning module"""
from unittest.mock import patch
import pandas as pd
from life_expectancy.cleaning import main
from life_expectancy.data_process import load_data, save_data
from . import OUTPUT_DIR


def test_clean_data(eu_life_expectancy_raw, uk_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""

    uk_life_expectancy_actual = main('UK', eu_life_expectancy_raw)
    pd.testing.assert_frame_equal(
        uk_life_expectancy_actual, uk_life_expectancy_expected
    )

# Unit tests

def test_load_data():
    """Run the `load_data` function and check if the output is not empty dataframe"""
    actual_result = load_data()

    assert isinstance(actual_result, pd.DataFrame)
    assert not actual_result.empty

def test_save_data():
    """Run the `save_data` function and check the filtering and saving methods"""
    cleaned_data = pd.DataFrame({
        'unit': ['YR', 'YR'],
        'sex': ['F', 'F'],
        'age': ['Y25', 'Y65'],
        'region': ['UK', 'PT'],
        'year': [2018, 2021],
        'value': [58.6, 21.7]
    })

    region = 'UK'

    # Patch the to_csv method to print a simple message instead of writing to a file
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:

        mock_to_csv.return_value = print("Mocked to_csv called!")

        actual_result = save_data(cleaned_data,region)

        expected_result = cleaned_data[cleaned_data['region'] == region]

        # Assertions
        pd.testing.assert_frame_equal(
            actual_result.reset_index(drop=True), expected_result.reset_index(drop=True)
            )

        # Assert that the to_csv method was called with the correct arguments
        mock_to_csv.assert_called_once_with(
            OUTPUT_DIR / f"{region.lower()}_life_expectancy.csv",
            index=False
        )
