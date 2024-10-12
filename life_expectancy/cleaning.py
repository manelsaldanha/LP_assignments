"""
Data cleaning script used to clean the eu_life_expectancy_raw.tsv file.
"""
from pathlib import Path
import argparse
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

def save_data(cleaned_data: pd.DataFrame, region: str) -> None:
    """
    Saves the cleaned data for a specific region to a CSV file.

    Parameters:
    cleaned_data (pd.DataFrame): The cleaned data to be saved.
    region (str): The country code used to filter and name the output file.

    Returns:
    None
    """
    data_filtered_by_region = cleaned_data[cleaned_data['region'] == region]

    data_filtered_by_region.to_csv(
        PROJECT_DIR / 'data' / f"{region.lower()}_life_expectancy.csv",
        index=False
    )


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
    data['year'] = data['year'].astype(int)
    data['value'] = data['value'].astype(float)

    return data


def main(region: str) -> None:
    """
    Orchestrates the data processing workflow. Loads raw life expectancy data,
    cleans it, and saves the cleaned data for the specified region.

    Parameters:
    region (str): Country code for which to save the cleaned data. Default is 'PT'.

    Returns:
    None
    """
    data_raw = load_data()
    cleaned_data = clean_data(data_raw)

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

    main(args.country)
