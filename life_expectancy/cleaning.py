"""
Data cleaning script used to clean the eu_life_expectancy_raw.tsv file.
"""
from typing import Optional
import argparse
import pandas as pd
from .data_process import load_data, save_data

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw life expectancy data.

    Parameters:
    data (pd.DataFrame): The raw data to be cleaned.

    Returns:
    pd.DataFrame: The cleaned DataFrame ready for analysis.
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

    return data


def main(region: str, data_raw: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Orchestrates the data processing workflow. Loads raw life expectancy data,
    cleans it, and saves the cleaned data for the specified region.

    Parameters:
    region (str): Country code for which to save the cleaned data. Default is 'PT'.

    Returns:
    None
    """
    if data_raw is None:
        data_raw = load_data()

    cleaned_data = clean_data(data_raw)

    data_filtered_by_region = save_data(cleaned_data, region)

    return data_filtered_by_region.reset_index(drop=True)


if __name__ == "__main__":  # pragma: no cover

    parser = argparse.ArgumentParser(description="Clean data for a specific country.")

    # Add the country argument with a default value of "PT"
    parser.add_argument(
        "-c", "--country",
        default="PT",
        help="Specify the country code to clean data for. Default is 'PT'."
    )
    args = parser.parse_args()

    main(args.country)
