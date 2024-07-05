FROM python:3.8-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    fonts-liberation \
    libappindicator3-1 \
    libxkbcommon-x11-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY api/requirements.txt /app/api/requirements.txt
RUN pip3 install --no-cache-dir -r /app/api/requirements.txt

# Copy the rest of the application code
COPY . /app

# Make sure Python buffer is set to unbuffered to capture logs
ENV PYTHONUNBUFFERED=1

CMD ["python3", "scripts/pipeline.py"]
