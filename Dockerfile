FROM python:3.10

WORKDIR /app

# Install all requirements
COPY api/requirements.txt /app/api_requirements.txt
COPY ui/requirements.txt /app/ui_requirements.txt
RUN cat /app/api_requirements.txt /app/ui_requirements.txt > /app/requirements.txt \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apt-get update && apt-get install -y curl # 👈 Need 'curl' for the health check

# Copy all application code
COPY . /app

# Make the start script executable
RUN chmod +x /app/start.sh

# Expose the single port that the UI will use (Hugging Face exposed port)
EXPOSE 7860
EXPOSE 8001 # Expose the internal port too (optional, but good practice)

# Run the start script as the main process
CMD ["/app/start.sh"]