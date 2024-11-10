"""Loading and Saving Functions"""
from pathlib import Path
from typing import Callable
import pandas as pd
from .region_enum import Region

PROJECT_DIR = Path(__file__).parents[0]

FileLoadingStrategy = Callable[[], pd.DataFrame]

def load_tsv_strategy() -> pd.DataFrame:
    """
    Loads raw life expectancy data from a TSV file.

    Returns:
    pd.DataFrame: DataFrame containing the raw data from the TSV file.
    """
    return pd.read_csv(PROJECT_DIR / 'data' / "eu_life_expectancy_raw.tsv", sep='\t')

def load_json_strategy() -> pd.DataFrame:
    """
    Loads raw life expectancy data from a JSON file.

    Returns:
    pd.DataFrame: DataFrame containing the raw data from the JSON file.
    """
    return pd.read_json(PROJECT_DIR / 'data' / "eurostat_life_expect.json")

def load_data(loading_strategy: FileLoadingStrategy) -> pd.DataFrame:
    """
    Loads data using the specified loading strategy function.

    Parameters:
    loading_strategy (FileLoadingStrategy): A function that defines how to load the data.

    Returns:
    pd.DataFrame: The loaded raw data as a DataFrame.
    """

    return loading_strategy()

def save_data(cleaned_data: pd.DataFrame, region: Region) -> pd.DataFrame:
    """
    Saves the cleaned data for a specific region to a CSV file.

    Parameters:
    cleaned_data (pd.DataFrame): The cleaned data to be saved.
    region (str): The country code used to filter and name the output file.

    Returns:
    pd.DataFrame: The data filtered by region as a DataFrame
    """
    data_filtered_by_region = cleaned_data[cleaned_data['region'] == region.value] \
        .reset_index(drop=True)

    data_filtered_by_region.to_csv(
        PROJECT_DIR / 'data' / f"{region.value.lower()}_life_expectancy.csv",
        index=False
    )

    return data_filtered_by_region
