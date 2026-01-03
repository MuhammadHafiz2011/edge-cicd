FROM python:3.11-slim

WORKDIR /app

COPY gateway.py .

RUN pip install --no-cache-dir flask requests

CMD ["python", "gateway.py"]
