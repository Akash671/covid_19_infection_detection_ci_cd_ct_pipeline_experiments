from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

app = FastAPI()

# --- Pydantic Input Model Definition (CRITICAL FIX for 422 Error) ---
# This model ensures FastAPI reads the JSON body data sent by the Streamlit app.
class PredictionInput(BaseModel):
    age: float
    fever: float
    lung: int
    fatigue: float

# --- MODEL LOADING WITH PATHLIB ---
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("INFO: Model loaded successfully!")
except FileNotFoundError:
    print(f"ERROR: Model file not found at: {MODEL_PATH}")
    raise
# --- END MODEL LOADING ---


@app.post("/predict")
# The function now accepts the Pydantic model object 'data'
def predict(data: PredictionInput):
    
    # Extract values from the Pydantic object
    age = data.age
    fever = data.fever
    lung = data.lung
    fatigue = data.fatigue
    
    # 1. Create a dictionary with feature names matching training data
    # CRITICAL: Keys match the feature names seen during model training (e.g., 'Age', 'Fever_C').
    input_data = {
        'Age': [age],
        'Fever_C': [fever],
        'Chronic_Lung_Disease': [lung],
        'Fatigue_Level': [fatigue]
    }
    
    # 2. Convert to a pandas DataFrame (required to pass feature names to the model).
    X = pd.DataFrame(input_data) 
    
    # Perform prediction
    pred = model.predict(X)[0]

    # If model supports probability
    try:
        prob = model.predict_proba(X)[0][1]
    except AttributeError:
        # Fallback if the model does not have predict_proba
        prob = float(pred)

    return {
        "prediction": int(pred),
        "probability": float(prob)
    }

@app.get("/")
def home():
    return {"message": "FastAPI backend running"}