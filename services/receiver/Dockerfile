FROM python:3.11-slim

WORKDIR /app

COPY receiver.py .

RUN pip install paho-mqtt requests

CMD ["python", "-u", "receiver.py"]


