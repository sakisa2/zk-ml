import csv
from pathlib import Path
import os

import sys
from poseidon_py.poseidon import poseidon_hash

# Ulazni CSV fajl (prvih 50 redova sa pacijentima)
INPUT_CSV = Path("data/patients.csv")

# Izlazni fajlovi
HASHES_FILE = Path("hashes/patient_hashes.txt")
COMMITMENT_FILE = Path("hashes/commitment.txt")

# Funkcija za enkodovanje reda u niz celih brojeva
def encode_patient(row):
    pol = int(row["pol"])
    starost = int(row["starost"])
    pritisak = int(float(row["pritisak"]) * 1000)
    holesterol = int(float(row["holesterol"]) * 1000)
    dijagnoza = int(row["dijagnoza"])
    return [pol, starost, pritisak, holesterol, dijagnoza]

# Heš funkcija koja koristi Poseidon
def hash_patient(data):
    return poseidon_hash(data)

# Kreiranje direktorijuma ako ne postoje
HASHES_FILE.parent.mkdir(parents=True, exist_ok=True)

# Glavna logika
hashes = []
with open(INPUT_CSV, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Preskoči red ako bilo koje polje nedostaje (prazan string)
        if not all([row["pol"], row["starost"], row["pritisak"], row["holesterol"], row["dijagnoza"]]):
            continue

        encoded = encode_patient(row)
        h = hash_patient(encoded)
        hashes.append(h)

        if len(hashes) == 50:
            break

# Upisivanje svih heševa u txt fajl
with open(HASHES_FILE, "w") as f:
    for h in hashes:
        f.write(str(h) + "\n")

# Commitment: Poseidon heš svih heševa zajedno
commitment = hashes[0]
for h in hashes[1:]:
    commitment = poseidon_hash([commitment, h])

with open(COMMITMENT_FILE, "w") as f:
    f.write(str(commitment))

print(f"✅ Commitment generated: {commitment}")
print(f"🔐 Hashes saved to {HASHES_FILE}")
print(f"📦 Commitment saved to {COMMITMENT_FILE}")
