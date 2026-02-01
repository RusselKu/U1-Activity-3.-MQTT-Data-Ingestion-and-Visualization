FROM apache/airflow:2.8.1

# system dependencies 
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# user
USER airflow

# python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /opt/airflow