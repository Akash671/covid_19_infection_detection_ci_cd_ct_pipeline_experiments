#!/bin/bash

# --- 1. Start FastAPI in the background on port 8001 ---
echo "Starting FastAPI on port 8001 in the background..."
# Note: api.main is the Python module path, :app is the FastAPI object name
uvicorn api.main:app --host 0.0.0.0 --port 8001 &

# Store the process ID of the background job
FASTAPI_PID=$!

# --- 2. Wait for FastAPI to be fully ready ---
echo "Waiting for FastAPI to become ready on http://127.0.0.1:8001..."
ATTEMPTS=0
MAX_ATTEMPTS=20  # Give it up to 20 seconds to start
until curl -s http://127.0.0.1:8001/health > /dev/null || [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; do
    echo "FastAPI not ready yet. Waiting 1 second..."
    sleep 1
    ATTEMPTS=$((ATTEMPTS + 1))
done

if [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; then
    echo "ERROR: FastAPI failed to start after $MAX_ATTEMPTS seconds. Check logs for dependencies/errors."
    kill $FASTAPI_PID # Kill the background process
    exit 1
fi

echo "FastAPI is running. Starting Streamlit..."

# --- 3. Start Streamlit in the foreground on port 7860 ---
# This is the main process the container monitors and MUST run on the app_port (7860)
streamlit run ui/streamlit_app.py --server.port 7860 --server.address 0.0.0.0

# Optional: Wait for the background process to finish if the foreground process dies
wait $FASTAPI_PID