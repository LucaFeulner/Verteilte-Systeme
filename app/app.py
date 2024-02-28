from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Umgebungsvariablen aus der .env-Datei laden

app = Flask(__name__)

COUCHDB_URL = os.getenv("COUCHDB_URL")

@app.route('/api/v1/get_data', methods=['GET'])
def get_data():
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)
    # CouchDB erwartet den Monat im Bereich 0-11
    month -= 1
    query = {
        "selector": {
            "month": {"$eq": month},
            "day": {"$eq": day}
        },
        "fields": ["name", "profession", "born"]
    }
    response = requests.post(f"{COUCHDB_URL}/_find", json=query)
    if response.status_code == 200:
        data = response.json()['docs']
        # Geburtstag in deutscher Schreibweise umwandeln
        for entry in data:
            entry['born'] = entry['born'].replace('-', '.')
        return jsonify(data), 200
    else:
        return jsonify({"error": "An error occurred"}), response.status_code

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_RUN_PORT', 8001))

