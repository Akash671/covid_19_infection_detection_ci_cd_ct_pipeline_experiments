import pandas as pd

def clean_data(df: pd.DataFrame):
    """
    Handle cleaning tasks:
    - drop irrelevant cols
    - handle nulls (example: drop or fill)
    """
    if "Sample ID" in df.columns:
        df = df.drop("Sample ID", axis=1)

    # Example: fill missing values with median
    df = df.fillna(df.median())

    return df
