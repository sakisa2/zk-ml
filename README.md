# zk-ml

Zero-knowledge proof of concept for private machine learning inference.

This project demonstrates how a simple ML forward pass can be executed
inside a Noir zero-knowledge circuit and proven with a zk-SNARK,
without revealing the input data (and optionally the model weights).

## Current status
Prototype

## Tech stack
- Noir + Nargo (circuit definition and proving)
- Poseidon (commitments)
- Python (commitment handling, backend logic)
- Minimal web frontend for demo interaction

## Implemented
- Input and weight commitments
- Forward pass computation inside the ZK circuit
- Proof generation and local verification

## Planned improvements
- Support for a concrete small model (MLP / tabular classifier)
- Constraint count optimization
- On-chain verifier deployment
- Integration experiments with zkML libraries (e.g. EZKL)


MIT License
