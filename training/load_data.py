import pandas as pd
from pathlib import Path
from typing import Union

def load_data(path: Union[str, Path]):
    """Load dataset from CSV."""
    df = pd.read_csv(path)
    return df
