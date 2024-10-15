"""Loading and Saving Functions"""
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).parents[0]

def load_data() -> pd.DataFrame:
    """
    Loads the raw life expectancy data from a TSV file and returns it as a DataFrame.

    Returns:
    pd.DataFrame: The loaded raw data.
    """
    raw_data = pd.read_csv(PROJECT_DIR / 'data' / "eu_life_expectancy_raw.tsv", sep='\t')

    return raw_data

def save_data(cleaned_data: pd.DataFrame, region: str) -> pd.DataFrame:
    """
    Saves the cleaned data for a specific region to a CSV file.

    Parameters:
    cleaned_data (pd.DataFrame): The cleaned data to be saved.
    region (str): The country code used to filter and name the output file.

    Returns:
    None
    """
    data_filtered_by_region = cleaned_data[cleaned_data['region'] == region].reset_index(drop=True)

    data_filtered_by_region.to_csv(
        PROJECT_DIR / 'data' / f"{region.lower()}_life_expectancy.csv",
        index=False
    )

    return data_filtered_by_region
