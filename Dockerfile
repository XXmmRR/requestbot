FROM python:3.13.7-slim-bookworm

WORKDIR /app

RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN pip install uv && \
    uv sync --cache-dir /opt/uv-cache
    
COPY . /app

RUN chmod +x /app/entrypoint.sh
    
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "main.py"]