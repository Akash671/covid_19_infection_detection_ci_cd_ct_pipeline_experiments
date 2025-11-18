FROM python:3.10

WORKDIR /app

# Combine all requirements for simplicity in this case
# Assuming you have a combined_requirements.txt or use the separate ones
COPY api/requirements.txt /app/api_requirements.txt
COPY ui/requirements.txt /app/ui_requirements.txt
RUN cat /app/api_requirements.txt /app/ui_requirements.txt > /app/requirements.txt \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy all application code
COPY . /app

# Create a start script (start.sh)
RUN echo '#!/bin/bash' > /app/start.sh \
    && echo 'uvicorn api.main:app --host 0.0.0.0 --port 8001 &' >> /app/start.sh \
    && echo 'streamlit run ui/streamlit_app.py --server.port 7860 --server.address 0.0.0.0' >> /app/start.sh \
    && chmod +x /app/start.sh

# Expose the single port that the UI will use (this is the only one Space cares about)
EXPOSE 7860

# Run the start script
CMD ["/app/start.sh"]