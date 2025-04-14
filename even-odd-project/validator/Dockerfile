# validator/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY validator/valid.sh /app/valid.sh
COPY . /app

RUN chmod +x /app/valid.sh
RUN pip install --no-cache-dir ruff isort mypy

ENTRYPOINT ["sh", "/app/valid.sh"]
