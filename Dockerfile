FROM python:3.9-slim

WORKDIR /app

COPY api/ .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p files

EXPOSE 5000

CMD ["python", "app.py"]
