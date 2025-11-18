import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess(df: pd.DataFrame):
    """Split data into X, y and train-test."""

    X = df.drop("Infected", axis=1)
    y = df["Infected"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y
    )
    return X_train, X_test, y_train, y_test
