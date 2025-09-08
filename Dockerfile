FROM python:3.13.7-slim-bookworm


WORKDIR /app


COPY pyproject.toml uv.lock ./

RUN pip install uv && \
    uv sync && \
    rm -rf /root/.cache/uv


COPY . /app


RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

    
    
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "main.py"]
