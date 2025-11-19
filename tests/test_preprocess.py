from training.feature_engineering import preprocess
from training.load_data import load_data
from training.data_cleaning import clean_data

def test_preprocess():
    df = load_data("data/raw/covid_19_data.csv")
    df = clean_data(df)
    X_train, X_test, y_train, y_test = preprocess(df)

    assert len(X_train) > 0
    assert len(X_test) > 0
    assert len(y_train) > 0
    assert len(y_test) > 0
