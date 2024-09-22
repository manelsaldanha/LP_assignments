"""
Data cleaning script used to clean the eu_life_expectancy_raw.tsv file.
"""
from pathlib import Path
import argparse
import pandas as pd

PROJECT_DIR = Path(__file__).parents[0]

def clean_data(region: str) -> None:
    """
    This function cleans the data for the specified country.
    :param country: The country code to filter the data (default is "PT").
    """

    # Load the TSV file into a DataFrame
    df = pd.read_csv(PROJECT_DIR / 'data' / "eu_life_expectancy_raw.tsv", sep='\t')

    # Split the first column into separate columns: 'unit', 'sex', 'age', 'region'
    df[['unit', 'sex', 'age', 'region']] = df['unit,sex,age,geo\\time'].str.split(',', expand=True)

    # Drop the original composed column
    df = df.drop(columns=['unit,sex,age,geo\\time'])

    # Unpivot (melt) the dataframe to get 'year' and 'value' columns
    df = df.melt(id_vars=['unit', 'sex', 'age', 'region'], var_name='year', value_name='value')

    # Remove the values in the df 'value' column that as a ' e' suffix
    df['value'] = df['value'].str.replace(r'\s.*$', '', regex=True)

    # Ensure the 'year' and 'value' columns have numeric values and clean it they dont
    df[['year', 'value']] = df[['year', 'value']].apply(pd.to_numeric, errors='coerce')

    # Drop rows where either 'year' or 'value' are NaN
    df = df.dropna(subset=['year', 'value'])

    # Convert the 'year' column to an integer and 'value' to a float
    df['year'] = df['year'].astype(int)
    df['value'] = df['value'].astype(float)

    final_df = df[df['region'] == region]
    final_df.to_csv(PROJECT_DIR / 'data' / f"{region.lower()}_life_expectancy.csv", index=False)


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

    clean_data(args.country)
