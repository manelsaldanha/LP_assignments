"""
Data cleaning script used to clean the eu_life_expectancy_raw.tsv file.
"""
from pathlib import Path
import argparse
import pandas as pd

PROJECT_DIR = Path(__file__).parents[0]

def load_data() -> pd.DataFrame:

    data = pd.read_csv(PROJECT_DIR / 'data' / "eu_life_expectancy_raw.tsv", sep='\t')

    return data

def save_data(data: pd.DataFrame, region: str) -> None:

    data_filtered_by_region = data[data['region'] == region]

    data_filtered_by_region.to_csv(
        PROJECT_DIR / 'data' / f"{region.lower()}_life_expectancy.csv",
        index=False
    )


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    This function cleans the data for the specified country.
    :param country: The country code to filter the data (default is "PT").
    """

    # Split the first column into separate columns: 'unit', 'sex', 'age', 'region'
    data[['unit', 'sex', 'age', 'region']] = (
        data['unit,sex,age,geo\\time'].str.split(',', expand=True)
    )

    # Drop the original composed column
    data = data.drop(columns=['unit,sex,age,geo\\time'])

    # Unpivot (melt) the dataframe to get 'year' and 'value' columns
    data = data.melt(id_vars=['unit', 'sex', 'age', 'region'], var_name='year', value_name='value')

    # Remove the values in the data 'value' column that as a ' e' suffix
    data['value'] = data['value'].str.replace(r'\s.*$', '', regex=True)

    # Ensure the 'year' and 'value' columns have numeric values and clean it they dont
    data[['year', 'value']] = data[['year', 'value']].apply(pd.to_numeric, errors='coerce')

    # Drop rows where either 'year' or 'value' are NaN
    data = data.dropna(subset=['year', 'value'])

    # Convert the 'year' column to an integer and 'value' to a float
    data['year'] = data['year'].astype(int)
    data['value'] = data['value'].astype(float)

    return data


# Main function to orchestrate loading, cleaning, and saving
def main(region: str) -> None:
    data_raw = load_data()
    data_clean = clean_data(data_raw)
    save_data(data_clean, region)


if __name__ == "__main__":  # pragma: no cover
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Clean data for a specific country.")

    # Add the country argument with a default value of "PT"
    parser.add_argument(
        "-c", "--country",
        default="PT",
        help="Specify the country code to clean data for. Default is 'PT'."
    )

    # Parse command-line arguments
    args = parser.parse_args()

    main(args.country)
