# services/even-service/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY services/even_service /app/even_service

RUN pip install --no-cache-dir -r /app/even_service/requirements.txt

CMD ["python", "-m", "even_service.even_service"]
