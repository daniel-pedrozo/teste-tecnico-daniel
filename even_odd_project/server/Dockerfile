# server/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY . /app/server

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r server/requirements.txt

CMD ["uvicorn", "server.server:app", "--host", "0.0.0.0", "--port", "8000"]