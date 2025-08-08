from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from poseidon_py.poseidon import poseidon_hash
import csv, os, toml
import subprocess


app = Flask(__name__)
CORS(app)

INPUT_CSV = Path("data/patients.csv")
HASHES_FILE = Path("hashes/patient_hashes.txt")
COMMITMENT_FILE = Path("hashes/commitment.txt")
PROVER_FILE = Path("Prover.toml")
CSV_FILE = "Prover.csv"
SCRIPT_FILE = Path(__file__).parent / "skripta.sh"


def encode_patient(row):
    pol = int(row["pol"])
    starost = int(row["starost"])
    pritisak = int(float(row["pritisak"]) * 1000)
    holesterol = int(float(row["holesterol"]) * 1000)
    dijagnoza = int(row["dijagnoza"])
    return [pol, starost, pritisak, holesterol, dijagnoza]

def hash_patient(data):
    return poseidon_hash(data)

def load_training(limit=50):
    HASHES_FILE.parent.mkdir(parents=True, exist_ok=True)
    hashes, training_notes = [], []
    with open(INPUT_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not all([row["pol"], row["starost"], row["pritisak"], row["holesterol"], row["dijagnoza"]]):
                continue
            encoded = encode_patient(row)
            training_notes.append(encoded)
            hashes.append(hash_patient(encoded))
            if len(hashes) == limit:
                break
    with open(HASHES_FILE, "w") as f:
        for h in hashes:
            f.write(hex(h) + "\n")
    return training_notes

def compute_commitment(training_notes):
    commitment = poseidon_hash(training_notes[0])
    for encoded in training_notes[1:]:
        commitment = poseidon_hash([commitment] + encoded)
    with open(COMMITMENT_FILE, "w") as f:
        f.write(hex(commitment))
    return commitment

def save_prover_inputs(training_notes, commitment, q, salt, k, filename):
    lines = []
    for i, note in enumerate(training_notes, start=1):
        lines.append(f'p{i} = [{", ".join(str(x) for x in note)}]')
    lines.append(f'q = [{q[0]}, {q[1]}, {q[2]}, {q[3]}]')
    lines.append(f'salt = "{salt}"')
    commit_hex = "0x" + format(commitment, "064x")
    salt_commit = poseidon_hash([int(salt)])
    salt_commit_hex = "0x" + format(salt_commit, "064x")
    lines.append(f'public_inputs = ["{commit_hex}", {k}, "{salt_commit_hex}"]')
    with open(filename, "w") as f:
        f.write("\n".join(lines))
    return commit_hex, salt_commit_hex

@app.route("/api/run-script", methods=["POST"])
def run_script():
    try:
        payload = request.get_json() or {}
        cp = subprocess.run(
            ["bash", str(SCRIPT_FILE)],
            cwd=str(SCRIPT_FILE.parent),
            capture_output=True,
            text=True,
            check=True,
        )
        return jsonify({"ok": True, "stdout": cp.stdout, "stderr": cp.stderr})
    except subprocess.CalledProcessError as e:
        return jsonify({"ok": False, "code": e.returncode, "stdout": e.stdout, "stderr": e.stderr}), 500


@app.route("/api/predict", methods=["POST"])
def generate_prover():
    data = request.get_json()
    pol = int(data["pol"])
    starost = int(data["starost"])
    pritisak = int(float(data["pritisak"]) * 1000)
    holesterol = int(float(data["holesterol"]) * 1000)
    salt = str(data["salt"])
    k = int(data.get("k", 3))

    training_notes = load_training()
    commitment = compute_commitment(training_notes)
    q = [pol, starost, pritisak, holesterol]
    commit_hex, salt_commit_hex = save_prover_inputs(training_notes, commitment, q, salt, k, PROVER_FILE)

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["pol", "starost", "pritisak", "holesterol", "salt", "k"])
        writer.writerow([pol, starost, pritisak, holesterol, salt, k])

    return jsonify({
        "ok": True,
        "commitment_hex": commit_hex,
        "salt_commit_hex": salt_commit_hex,
        "prover_file": str(PROVER_FILE)
    })

@app.route('/api/predict', methods=['GET'])
def predict_get():
    return jsonify({"message": "GET ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
