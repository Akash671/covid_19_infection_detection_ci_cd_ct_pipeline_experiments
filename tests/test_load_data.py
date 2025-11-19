import pandas as pd
from training.load_data import load_data

def test_load_data():
    df = load_data("data/raw/covid_19_data.csv")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
