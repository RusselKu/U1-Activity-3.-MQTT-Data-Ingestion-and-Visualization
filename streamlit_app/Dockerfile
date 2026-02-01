FROM python:3.9-slim

WORKDIR /app

# dependencies 
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# path
ENV PATH="/root/.local/bin:${PATH}"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --user --timeout=600 -r requirements.txt


COPY . .

#port
EXPOSE 8501

# HEALTHCHECK 
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando para ejecutar la app
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py", "--server.port=8501", "--server.address=0.0.0.0"]