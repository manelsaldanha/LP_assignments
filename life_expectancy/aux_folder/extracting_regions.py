"""Script that extracts all the regions"""
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).parents[1]

raw_data = pd.read_csv(PROJECT_DIR / "data" / "eu_life_expectancy_raw.tsv", sep='\t')

raw_data[['unit', 'sex', 'age', 'region']] = (
        raw_data['unit,sex,age,geo\\time'].str.split(',', expand=True)
    )

data = raw_data.drop(columns=['unit,sex,age,geo\\time'])
data = data.melt(id_vars=['unit', 'sex', 'age', 'region'], var_name='year', value_name='value')

# get all the unique regions inside eu_life_expectancy_raw.tsv
print(data['region'].unique().tolist())

