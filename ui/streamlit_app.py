import streamlit as st
import requests

# NOTE: Ensure this URL and port match your Uvicorn server (e.g., 8001)
FASTAPI_URL = "http://127.0.0.1:8001/predict" 

st.set_page_config(
    page_title="COVID-19 Infection Detection",
    layout="centered"
)

st.title("🦠 COVID-19 Infection Detection ML App")
st.write("Enter patient details below to predict infection probability.")

st.markdown("---")

age = st.number_input("Age", min_value=1, max_value=120)
fever = st.number_input("Fever (°C)", min_value=33.0, max_value=45.0)
lung = st.number_input("Chronic Lung Disease (0 or 1)", min_value=0, max_value=1)
fatigue = st.slider("Fatigue Level (0 = none, 10 = high)", 0, 10, key="fatigue_slider")

if st.button("Predict Infection"):
    with st.spinner("Analyzing..."):
        # CRITICAL: These keys must match the parameter names in the FastAPI Pydantic model
        # (age, fever, lung, fatigue) as defined in api/main.py.
        data_payload = {
            "age": age,
            "fever": fever,
            "lung": lung,
            "fatigue": fatigue
        }

        try:
            # FIX: Send data in the request body using 'json=' 
            response = requests.post(FASTAPI_URL, json=data_payload)
            
            # 1. Successful response (200 OK)
            if response.status_code == 200:
                data = response.json()
                result = data["prediction"]
                prob = data["probability"]

                if result == 1:
                    st.error(f"⚠️ Patient likely infected! (Probability: {prob:.2f})")
                else:
                    st.success(f"✔ Patient unlikely infected. (Probability: {prob:.2f})")
            
            # 2. Server Error (4xx or 5xx)
            else:
                error_message = f"Backend API Error (Status: {response.status_code})."
                try:
                    # Attempt to get JSON error details from FastAPI
                    error_details = response.json().get("detail", response.text)
                    error_message += f"\nDetails: {error_details}"
                except requests.exceptions.JSONDecodeError:
                    error_message += f"\nRaw Response: {response.text}"
                
                st.error(error_message)


        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to backend API at {FASTAPI_URL}. Ensure FastAPI is running on the correct port and accessible.")
        except Exception as e:
            st.error(f"An unexpected error occurred during prediction: {str(e)}")


st.markdown("---")
st.caption("Powered by FastAPI + Streamlit + ML + HuggingFace Spaces")