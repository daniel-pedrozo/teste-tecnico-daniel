# services/odd-service/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY ./services/odd_service /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "odd_service.py"]
