"""
Data cleaning script used to clean the eu_life_expectancy_raw.tsv file.
"""
import argparse
from typing import Callable
import pandas as pd
from .data_process import load_data, load_json_strategy, save_data
from .region_enum import Region

FileCleaningStrategy = Callable[[pd.DataFrame], pd.DataFrame]

def clean_json_strategy(data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans data loaded from a JSON file.

    Parameters:
    data (pd.DataFrame): Raw JSON data to be cleaned.

    Returns:
    pd.DataFrame: Cleaned DataFrame with renamed columns.
    """
    data = data.drop(columns=["flag", "flag_detail"])
    data = data.rename(columns={"country": "region", "life_expectancy": "value"})
    return data

def clean_tsv_strategy(data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans data loaded from a TSV file containing life expectancy information.

    Parameters:
    data (pd.DataFrame): Raw TSV data to be cleaned.

    Returns:
    pd.DataFrame: Cleaned DataFrame with structured columns and numeric values.
    """
    # Clean data process
    data[['unit', 'sex', 'age', 'region']] = (
        data['unit,sex,age,geo\\time'].str.split(',', expand=True)
    )

    data = data.drop(columns=['unit,sex,age,geo\\time'])
    data = data.melt(id_vars=['unit', 'sex', 'age', 'region'], var_name='year', value_name='value')

    # Removes any characters from the first whitespace to the end of each string
    data['value'] = data['value'].str.replace(r'\s.*$', '', regex=True)
    data[['year', 'value']] = data[['year', 'value']].apply(pd.to_numeric, errors='coerce')
    data = data.dropna(subset=['year', 'value'])
    data['year'] = data['year'].astype('int64')
    data['value'] = data['value'].astype('float64')

    return data.reset_index(drop=True)

def clean_data(data: pd.DataFrame, cleaning_strategy: FileCleaningStrategy) -> pd.DataFrame:
    """
    Applies a specified cleaning strategy to the data.

    Parameters:
    data (pd.DataFrame): The raw data to be cleaned.
    cleaning_strategy (FileCleaningStrategy): The function to apply for cleaning.

    Returns:
    pd.DataFrame: Cleaned data.
    """
    return cleaning_strategy(data)


def main(region: Region) -> None:
    """
    Orchestrates the data processing workflow. Loads raw life expectancy data,
    cleans it, and saves the cleaned data for the specified region.

    Parameters:
    region (str): Country code for which to save the cleaned data. Default is 'PT'.

    Returns:
    None
    """
    data_raw = load_data(load_json_strategy)
    cleaned_data = clean_data(data_raw, clean_json_strategy)

    save_data(cleaned_data, region)


if __name__ == "__main__":  # pragma: no cover

    parser = argparse.ArgumentParser(description="Clean data for a specific country.")

    # Add the country argument with a default value of "PT"
    parser.add_argument(
        "-c", "--country",
        default="PT",
        help="Specify the country code to clean data for. Default is 'PT'."
    )
    args = parser.parse_args()

    main(Region[args.country])
