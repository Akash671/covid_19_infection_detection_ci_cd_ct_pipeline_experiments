FROM python:3.10

WORKDIR /app

COPY api/ /app/api/
RUN pip install --no-cache-dir -r /app/api/requirements.txt

COPY ui/ /app/ui/
RUN pip install --no-cache-dir -r /app/ui/requirements.txt

EXPOSE 8000
EXPOSE 7860

CMD uvicorn api.main:app --host 0.0.0.0 --port 8001 & \
    streamlit run ui/streamlit_app.py --server.port 7860 --server.address 0.0.0.0
