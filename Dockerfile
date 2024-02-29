# Verwenden Sie ein offizielles Python-Runtime-Image als Basis
FROM python:3.8-slim

# Legen Sie das Arbeitsverzeichnis im Container fest
WORKDIR /usr/src/app

# Kopieren Sie den Inhalt des aktuellen Verzeichnisses in den Container unter /usr/src/app
COPY . .

# Installieren Sie alle benötigten Pakete, die in requirements.txt angegeben sind
RUN pip install --no-cache-dir -r requirements.txt

# Machen Sie Port 8001 für die Außenwelt zugänglich
EXPOSE 8001

# Definieren Sie eine Umgebungsvariable
ENV FLASK_RUN_PORT=8001

# Führen Sie app.py aus, wenn der Container gestartet wird
CMD ["python", "./app/app.py"]
