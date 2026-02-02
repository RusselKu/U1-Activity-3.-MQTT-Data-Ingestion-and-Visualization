FROM python:3.11-slim-buster

# system dependencies 
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app