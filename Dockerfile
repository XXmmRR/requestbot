FROM 3.13.7-slim-bookworm

WORKDIR /app

COPY . /app

COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

RUN pip install uv && \
    uv pip install --no-cache-dir -r uv.lock && \
    rm -rf /root/.cache/uv

ENTRYPOINT ["entrypoint.sh"]
CMD ["python", "main.py"]