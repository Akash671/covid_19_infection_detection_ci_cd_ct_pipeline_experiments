FROM python:3.10-slim

# Install system dependencies (needed for 'curl' and sometimes ML libraries)
# We need 'curl' for the service readiness check in start.sh
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Combine and install all Python requirements first for efficient caching
COPY api/requirements.txt /app/api_requirements.txt
COPY ui/requirements.txt /app/ui_requirements.txt
# Concatenate the two requirement files and install
RUN cat /app/api_requirements.txt /app/ui_requirements.txt > /app/requirements.txt \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy all application code (API, UI, training, etc.)
# Note: Ensure your data files/models needed for the API are copied here!
COPY . /app

# Make the startup script executable
RUN chmod +x /app/start.sh

# Expose the ports. 7860 is the port Hugging Face will use to proxy traffic.
EXPOSE 7860
EXPOSE 8001

# Run the custom startup script
CMD ["/app/start.sh"]