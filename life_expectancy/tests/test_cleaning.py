"""Tests for the cleaning module"""
from unittest.mock import patch, Mock
import pandas as pd
from life_expectancy.cleaning import clean_data
from life_expectancy.data_process import load_data, save_data


def test_clean_data(eu_life_expectancy_raw, eu_life_expectancy_expected):
    """
    Run the `clean_data` function and compare the output to the expected output
    using the fixtures created in create_fixtures.py inside the aux folder
    """

    eu_life_expectancy_actual = clean_data(eu_life_expectancy_raw)
    pd.testing.assert_frame_equal(
        eu_life_expectancy_actual, eu_life_expectancy_expected
    )

@patch("life_expectancy.cleaning.pd.read_csv")
def test_load_data(read_csv_mock: Mock):
    """Run the `load_data` function and checking on a mock dataframe"""

    read_csv_mock.return_value = pd.DataFrame({"life_exp": [78, 79, 77]})
    actual_result = load_data()
    read_csv_mock.assert_called_once()

    pd.testing.assert_frame_equal(actual_result, read_csv_mock.return_value)

    assert isinstance(actual_result, pd.DataFrame)
    assert not actual_result.empty

def test_save_data():
    """
    Run the `save_data` function and check the filtering and saving methods
    on a mock dataframe
    """
    cleaned_data = pd.DataFrame({
        'unit': ['YR', 'YR'],
        'sex': ['F', 'F'],
        'age': ['Y25', 'Y65'],
        'region': ['UK', 'PT'],
        'year': [2018, 2021],
        'value': [58.6, 21.7]
    })

    # Patch the to_csv method to print a simple message instead of writing to a file
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:

        mock_to_csv.return_value = print("Mocked to_csv method!")

        actual_result = save_data(cleaned_data, 'PT')
        expected_result = cleaned_data[cleaned_data['region'] == 'PT'].reset_index(drop=True)
        pd.testing.assert_frame_equal(actual_result, expected_result)
        mock_to_csv.assert_called_once()
