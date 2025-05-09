FROM python:3.11-slim

# Installer les dépendances système nécessaires pour les notifications et le scraping
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libnotify-bin \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config ./config
COPY modules ./modules
COPY main.py .

CMD ["python", "main.py"]