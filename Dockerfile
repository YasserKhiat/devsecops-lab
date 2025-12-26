FROM python:3.9-slim

WORKDIR /app

# Copy only necessary files
COPY api/ .            
COPY requirements.txt . 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for safe file reading
RUN mkdir -p files

EXPOSE 5000

CMD ["python", "app.py"]
