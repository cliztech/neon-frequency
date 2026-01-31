FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files to ensure imports like 'core.brain...' work
COPY . .

# Set PYTHONPATH so that 'core' and other top-level folders are importable
ENV PYTHONPATH=/app

CMD ["python3", "core/brain/cortex.py"]
