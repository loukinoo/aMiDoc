# Usa un'immagine base con Python
FROM python:3.10-slim

# Installa Tesseract e dipendenze
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev poppler-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Crea e usa una directory app
WORKDIR /app

# Copia i file dell'app
COPY . .

# Installa dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Porta Flask su 0.0.0.0
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Espone la porta 8080 (usata da Railway)
EXPOSE 8080

# Comando per avviare l'app
CMD ["flask", "run", "--port=8080"]
