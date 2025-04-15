# services/even-service/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY ./services/even_service /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "even_service.py"]
