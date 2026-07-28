import joblib
import os
from datetime import datetime
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from training.load_data import load_data
from training.data_cleaning import clean_data
from training.feature_engineering import preprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "covid_19_data.csv"
RANDOM_STATE = 42


def train_model():

    # Load + Clean
    df = load_data(DATA_PATH)
    df = clean_data(df)

    # Preprocess
    X_train, X_test, y_train, y_test = preprocess(df)

    # Train
    model = RandomForestClassifier(random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # ---- SAVE MODEL WITH VERSION ----
    artifacts_dir = PROJECT_ROOT / "model_artifacts"
    api_dir = PROJECT_ROOT / "api"
    os.makedirs(artifacts_dir, exist_ok=True)
    os.makedirs(api_dir, exist_ok=True)

    version = datetime.now().strftime("%Y%m%d_%H%M%S")
    versioned_model_path = artifacts_dir / f"model_{version}.pkl"
    latest_model_path = artifacts_dir / "latest_model.pkl"
    api_model_path = api_dir / "model.pkl"

    # Save both versioned + latest
    joblib.dump(model, versioned_model_path)
    joblib.dump(model, latest_model_path)

    # Copy latest to API folder for deployment
    joblib.dump(model, api_model_path)

    print(f"✔ Saved versioned model: {versioned_model_path}")
    print(f"✔ Updated latest model: {latest_model_path}")
    print(f"✔ Deployed API model saved: {api_model_path}")
    print("Accuracy:", acc)

    return str(versioned_model_path), acc


if __name__ == "__main__":
    train_model()
