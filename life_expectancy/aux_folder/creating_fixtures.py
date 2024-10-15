"""Script that creates the input and expected fixture"""
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).parents[1]

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
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

raw_data = pd.read_csv(PROJECT_DIR / "data" / "eu_life_expectancy_raw.tsv", sep='\t')
input_feature = raw_data.sample(frac=0.1, random_state=42)
expected_feature = clean_data(input_feature)

input_feature.to_csv(
    PROJECT_DIR / "tests" / "fixtures" / "eu_life_expectancy_raw.tsv", sep='\t', index=False
    )
expected_feature.to_csv(
    PROJECT_DIR / "tests" / "fixtures" / "eu_life_expectancy_expected.csv", index=False
    )
