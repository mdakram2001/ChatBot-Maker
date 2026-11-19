#!/bin/bash
set -e

# Port for FastAPI internal backend
BACKEND_PORT=8000
export API_BASE_URL="http://127.0.0.1:${BACKEND_PORT}"

echo "Starting FastAPI backend on port ${BACKEND_PORT}..."
uvicorn chatamu.main:app --host 127.0.0.1 --port ${BACKEND_PORT} &

echo "Waiting for backend to initialize..."
sleep 3

echo "Starting Streamlit frontend on port ${PORT:-8501}..."
streamlit run frontend/app.py \
    --server.port=${PORT:-8501} \
    --server.address=0.0.0.0
