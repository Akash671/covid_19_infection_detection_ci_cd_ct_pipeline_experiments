from training.data_cleaning import clean_data
from training.load_data import load_data

def test_clean_data():
    df = load_data("data/raw/covid_19_data.csv")
    cleaned = clean_data(df)

    assert cleaned.isnull().sum().sum() == 0  # no nulls
    assert "Sample ID" not in cleaned.columns  # dropped feature
