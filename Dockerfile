FROM 3.13.7-slim-bookworm

WORKDIR /app

COPY . /app

RUN pip install uv && \
    uv pip install --no-cache-dir -r uv.lock && \
    rm -rf /root/.cache/uv

CMD ["python", "main.py"]