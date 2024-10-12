from pathlib import Path
import pandas as pd
from cleaning import clean_data

PROJECT_DIR = Path(__file__).parents[0]

# Load the full dataset
raw_data = pd.read_csv(PROJECT_DIR / "data" / "eu_life_expectancy_raw.tsv", sep='\t')

# Creating input fixture
input_feature = raw_data.sample(frac=0.1, random_state=42)

# Creating expected fixture
df_clean = clean_data(input_feature)
expected_feature = df_clean[df_clean["region"] == "PT"]

# Save the sample data as a new fixture
input_feature.to_csv(PROJECT_DIR / "tests" / "fixtures" / "eu_life_expectancy_raw.tsv", sep='\t', index=False)
expected_feature.to_csv(PROJECT_DIR / "tests" / "fixtures" / "eu_life_expectancy_expected.csv", index=False)
