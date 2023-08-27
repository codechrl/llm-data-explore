FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

RUN apt-get update

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 80