# validator/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY validator/valid.sh /app/valid.sh
COPY . /app

RUN pip install --no-cache-dir ruff isort mypy \
    && pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/valid.sh

ENTRYPOINT ["sh", "/app/valid.sh"]