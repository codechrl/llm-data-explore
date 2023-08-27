FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=1

CMD [ "streamlit", "run", "main.py", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.enableWebsocketCompression=false", "--server.baseUrlPath=extory"]
