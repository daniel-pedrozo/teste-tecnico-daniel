# services/odd-service/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY services/odd_service /app/odd_service

RUN pip install --no-cache-dir -r /app/odd_service/requirements.txt

CMD ["python", "-m", "odd_service.odd_service"]
