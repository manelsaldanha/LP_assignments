"""Script that creates the input and expected fixture"""
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).parents[1]

def clean_json_strategy(data: pd.DataFrame) -> pd.DataFrame:
    data = data.drop(columns=["flag", "flag_detail"])
    data = data.rename(columns={"country": "region", "life_expectancy": "value"})
    return data

raw_data = pd.read_json(PROJECT_DIR / "data" / "eurostat_life_expect.json")
input_feature = raw_data.sample(frac=0.1, random_state=42)
expected_feature = clean_json_strategy(input_feature)

input_feature.to_json(
    PROJECT_DIR / "tests" / "fixtures" / "eurostat_life_expect_raw.json", orient='records'
    )
expected_feature.to_csv(
    PROJECT_DIR / "tests" / "fixtures" / "eurostat_life_expect_expected.csv", index=False
    )
