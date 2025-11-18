---
title: COVID-19 Infection Detection ML App
emoji: 🦠
colorFrom: blue
colorTo: indigo
sdk: streamlit
# CRITICAL FIX: Explicitly set your Streamlit app file name
app_file: streamlit_app.py 
---

# 🚀 COVID-19 Detection Pipeline

This Hugging Face Space runs a two-part application:

1.  **Frontend:** A Streamlit application (`streamlit_app.py`).
2.  **Backend:** A FastAPI service (`api/main.py`) hosting the prediction model.

### Multi-Service Configuration

The `app` block below tells the Hugging Face environment to run the FastAPI service in the background on port 7860, and then start the Streamlit frontend, allowing them to communicate successfully.

```app
port: 7860
command: ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]