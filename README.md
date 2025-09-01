# Contraction Mapping Verification

![CI](https://github.com/towre676-cloud/contraction-mapping-verification/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A small, practical verifier for **contraction-mapping smallness conditions**.

It checks inequalities of the form:

- Core: `gamma * (1 + t * c_P) <= eps_threshold`
- Ledger (discrete): `gamma_k * (1 + t_k * c_P) * exp(-sigma * delta_tau_k) <= eps_threshold` (for all steps)
- Coupled streams: needs `min{kappa1,kappa2} > 2*sqrt(eta1*eta2)`; it reports `eps_eff = min - 2*sqrt(...)`

**Important:** In this tool, `eps` = the **threshold** on the left-hand side (LHS). The verifier checks `LHS <= eps`.  
If your paper uses `1 - ε`, translate that to a threshold or pass `--eps` yourself.

---

## Quick start (Windows, Git Bash)

1) Create & activate a venv
python -m venv .venv
source ./.venv/Scripts/activate

mathematica
Copy code

2) Install
pip install -r requirements.txt

mathematica
Copy code

3) Run the examples
python src/verify_gaps.py examples/core_banach/example_core.json --type core_banach --verified
python src/verify_gaps.py examples/ledger/example_ledger.json --type ledger --verified
python src/verify_gaps.py examples/coupled_streams/example_coupled.json --type coupled_stream

markdown
Copy code

Expected: all `OK`.

---

## CLI (abridged)
- `--type {core_banach, ledger, coupled_stream}`
- `--eps <float>`: override threshold
- `--tol <float>`: numeric tolerance
- `--verified`: outward rounding guards (`numpy.nextafter`)
- `--interval`: (planned) interval arithmetic
- `--use-gammaV`: (planned) SVD-based `||R @ Gamma||_2` bound

## Layout
src/verify_gaps.py
examples/
.github/workflows/ci.yml
paper/ (optional)

go
Copy code

MIT licensed. See `LICENSE`.
