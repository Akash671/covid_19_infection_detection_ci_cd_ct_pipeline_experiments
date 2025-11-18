#!/bin/bash

# --- 1. Start FastAPI in the background on port 8001 ---
echo "Starting FastAPI on port 8001..."
uvicorn api.main:app --host 0.0.0.0 --port 8001 &

# Store the process ID of the background job
FASTAPI_PID=$!

# --- 2. Wait for FastAPI to be fully ready ---
# This loop pings the API health check endpoint until it gets a response
echo "Waiting for FastAPI to be ready on 8001..."
ATTEMPTS=0
MAX_ATTEMPTS=15
until curl -s http://127.0.0.1:8001/health > /dev/null || [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; do
    echo "FastAPI not ready yet. Waiting 1 second..."
    sleep 1
    ATTEMPTS=$((ATTEMPTS + 1))
done

if [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; then
    echo "ERROR: FastAPI failed to start after $MAX_ATTEMPTS seconds."
    kill $FASTAPI_PID # Kill the background process
    exit 1
fi

echo "FastAPI is running. Starting Streamlit..."

# --- 3. Start Streamlit in the foreground on port 7860 ---
# This must be the LAST command and MUST run in the foreground (no &)
streamlit run ui/streamlit_app.py --server.port 7860 --server.address 0.0.0.0

# Cleanup (optional, but good practice)
wait $FASTAPI_PID # Wait for the FastAPI process to finish (which won't happen unless Streamlit exits)