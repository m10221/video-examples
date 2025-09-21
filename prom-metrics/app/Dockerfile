FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["python", "app.py"]
