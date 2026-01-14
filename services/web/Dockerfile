FROM python:3.11-slim

WORKDIR /app

COPY web_server.py .

RUN pip install flask

CMD ["python", "-u", "web_server.py"]
