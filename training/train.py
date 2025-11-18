import joblib
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from .load_data import load_data
from .data_cleaning import clean_data
from .feature_engineering import preprocess
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from load_data import load_data


def train_model():

    # Load + Clean
    df = load_data("data/raw/covid_19_data.csv")
    df = clean_data(df)

    # Preprocess
    X_train, X_test, y_train, y_test = preprocess(df)

    # Train
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # ---- SAVE MODEL WITH VERSION ----
    os.makedirs("model_artifacts", exist_ok=True)
    os.makedirs("api", exist_ok=True)

    version = datetime.now().strftime("%Y%m%d_%H%M%S")
    versioned_model_path = f"model_artifacts/model_{version}.pkl"
    latest_model_path = "model_artifacts/latest_model.pkl"
    api_model_path = "api/model.pkl"

    # Save both versioned + latest
    joblib.dump(model, versioned_model_path)
    joblib.dump(model, latest_model_path)

    # Copy latest to API folder for deployment
    joblib.dump(model, api_model_path)

    print(f"✔ Saved versioned model: {versioned_model_path}")
    print(f"✔ Updated latest model: {latest_model_path}")
    print(f"✔ Deployed API model saved: {api_model_path}")
    print("Accuracy:", acc)

    return versioned_model_path, acc


if __name__ == "__main__":
    train_model()
