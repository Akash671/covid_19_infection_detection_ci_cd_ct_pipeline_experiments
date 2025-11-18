#!/bin/bash

# --- 1. Start FastAPI in the background on port 8001 ---
echo "Starting FastAPI on port 8001 in the background..."
# CRITICAL FIX: Using 'python -m uvicorn' bypasses PATH issues.
python -m uvicorn api.main:app --host 0.0.0.0 --port 8001 &

# Store the process ID of the background job
FASTAPI_PID=$!

# --- 2. Wait for FastAPI to be fully ready ---
echo "Waiting for FastAPI to become ready on http://127.0.0.1:8001..."
ATTEMPTS=0
MAX_ATTEMPTS=20  # Give it up to 20 seconds
until curl -s http://127.0.0.1:8001/health > /dev/null || [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; do
    echo "FastAPI not ready yet. Waiting 1 second..."
    sleep 1
    ATTEMPTS=$((ATTEMPTS + 1))
done

if [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; then
    echo "ERROR: FastAPI failed to start after $MAX_ATTEMPTS seconds. Check logs for dependencies/errors."
    # The 'kill' command failed before because FASTAPI_PID was empty. Now we exit directly.
    exit 1
fi

echo "FastAPI is running. Starting Streamlit..."

# --- 3. Start Streamlit in the foreground on port 7860 ---
# CRITICAL FIX: Must run in the foreground on the port exposed by the Space.
python -m streamlit run ui/streamlit_app.py --server.port 7860 --server.address 0.0.0.0

# Optional: Wait for the background process to finish if the foreground process dies
wait $FASTAPI_PID