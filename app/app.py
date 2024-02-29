from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Umgebungsvariablen aus der .env-Datei laden
load_dotenv()

app = Flask(__name__)

# Umgebungsvariablen
COUCHDB_URL = os.getenv('COUCHDB_URL')
COUCHDB_DB = os.getenv('COUCHDB_DB')
COUCHDB_USER = os.getenv('COUCHDB_USER')
COUCHDB_PASSWORD = os.getenv('COUCHDB_PASSWORD')

# Authentifizierung für CouchDB
auth = (COUCHDB_USER, COUCHDB_PASSWORD)

@app.route('/api/v1/get_data', methods=['GET'])
def get_data():
    month = request.args.get('month')
    day = request.args.get('day')

    # Anpassung des Monats für die CouchDB-Anfrage (von 1-basiert auf 0-basiert)
    month_adjusted = str(int(month) - 1)

    query = {
        "selector": {
            "month": month_adjusted,
            "day": day
        },
        "fields": ["first","name","prof","year","month","day"],
        "sort": [{"year":"asc"}]
    }

    try:
        # POST-Anfrage an CouchDB mit Timeout
        response = requests.post(f"{COUCHDB_URL}/{COUCHDB_DB}/_find", json=query, auth=auth, timeout=2)



        if response.status_code == 200:
            data = response.json().get('docs', [])
            if data:
                # Formatieren der Antwort gemäß Aufgabenstellung
                formatted_data = [{"name": f"{d['first']} {d['name']}", "profession": d["prof"], "born": f"{d['day']}.{d['month']}.{d['year']}"} for d in data]
                return jsonify(formatted_data), 200
            else:
                return jsonify([]), 204
        elif response.status_code == 401:
            # Ungültige Anmeldeinformationen
            return jsonify({'error': 'Invalid credentials'}), 401


    except requests.exceptions.Timeout:
        # Timeout-Fehler
        return jsonify({'error': 'The request timed out'}), 408
    except Exception as e:
        # Allgemeine Fehler
        return jsonify({'error': 'An internal error occurred'}), 500



@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Service is up and running'}), 200

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=os.getenv('FLASK_RUN_PORT', 8001), debug=True)
