import csv
from pathlib import Path
import os
import toml
import sys
from poseidon_py.poseidon import poseidon_hash

INPUT_CSV = Path("data/patients.csv")
HASHES_FILE = Path("hashes/patient_hashes.txt")
COMMITMENT_FILE = Path("hashes/commitment.txt")
PROVER_FILE = Path("Prover.toml")

SALT = 1234567890123456789012345678901234567890

def encode_patient(row):
    pol = int(row["pol"])
    starost = int(row["starost"])
    pritisak = int(float(row["pritisak"]) * 1000)
    holesterol = int(float(row["holesterol"]) * 1000)
    dijagnoza = int(row["dijagnoza"])
    return [pol, starost, pritisak, holesterol, dijagnoza]

def hash_patient(data):
    return poseidon_hash(data)

HASHES_FILE.parent.mkdir(parents=True, exist_ok=True)

hashes = []
training_notes = []
with open(INPUT_CSV, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not all([row["pol"], row["starost"], row["pritisak"], row["holesterol"], row["dijagnoza"]]):
            continue
        encoded = encode_patient(row)
        training_notes.append(encoded)
        hashes.append(hash_patient(encoded))
        if len(hashes) == 50:
            break

with open(HASHES_FILE, "w") as f:
    for h in hashes:
        f.write(hex(h) + "\n")


commitment = poseidon_hash(training_notes[0])
for encoded in training_notes[1:]:
    tmp = [commitment] + encoded
    print(tmp)
    commitment = poseidon_hash(tmp)

    print(hex(commitment))

prover_inputs = {
    "inputs": {
        "training_notes": training_notes,
        "commitment_hash": hex(commitment)
    }
}

def save_prover_inputs_flat_x(training_notes, commitment, filename):
    lines = []
    # Privatni svedoci: 50 pacijenata
    for i, note in enumerate(training_notes, start=1):
        lines.append(f'p{i} = [{", ".join(str(x) for x in note)}]')

    # 2) Privatni upit q (tvoji simptomi) – ovde koristim p50 kao test;
    #    u produkciji upiši stvarni q koji stiže sa fronta.
    q0, q1, q2, q3 = training_notes[-1][0], training_notes[-1][1], training_notes[-1][2], training_notes[-1][3]
    lines.append(f'q = [{q0}, {q1}, {q2}, {q3}]')

    # 3) Privatni salt (int)
    lines.append(f'salt = "{SALT}"')

    # 4) Javni ulazi: commitment, k, salt_commit
    commit_hex = "0x" + format(commitment, "064x")
    k = 3  # promeni po potrebi (npr. iz fronta)
    salt_commit = poseidon_hash([SALT])
    salt_commit_hex = "0x" + format(salt_commit, "064x")

    # SADA public_inputs ima SAMO 3 polja: [commitment, k, salt_commit]
    lines.append(f'public_inputs = ["{commit_hex}", {k}, "{salt_commit_hex}"]')

    with open(filename, "w") as f:
        f.write("\n".join(lines))


save_prover_inputs_flat_x(training_notes, commitment, "Prover.toml")

print(f"Commitment generated: {commitment}")
print(f"Hashes saved to {HASHES_FILE}")
print(f"Commitment saved to {COMMITMENT_FILE}")
