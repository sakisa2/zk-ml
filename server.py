from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

CSV_FILE = "Prover.csv"

@app.route('/api/predict', methods=['POST'])
def predict_post():
    data = request.get_json()

    print("Primljeni podaci (POST):", data)

    # Izdvajanje vrednosti
    pol = data.get("pol")
    starost = data.get("starost")
    pritisak = data.get("pritisak")
    holesterol = data.get("holesterol")
    salt = data.get("salt")

    print("=== Vrednosti pojedinačno ===")
    print(pol, starost, pritisak, holesterol, salt)

    # Ako fajl ne postoji, napravi ga sa header-om
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["pol", "starost", "pritisak", "holesterol", "salt"])
        writer.writerow([pol, starost, pritisak, holesterol, salt])

    return jsonify({"message": "Podaci uspešno primljeni i upisani u Prover.csv"})

@app.route('/api/predict', methods=['GET'])
def predict_get():
    return jsonify({"message": "GET zahtev za testiranje"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)