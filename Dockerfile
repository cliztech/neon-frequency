FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV LIQUIDSOAP_HOST=liquidsoap
ENV AUDIO_CACHE_DIR=/audio_cache

# Run the application
CMD ["python3", "core/brain/cortex.py"]
