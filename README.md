# Contraction Mapping Verification

![CI](https://github.com/towre676-cloud/contraction-mapping-verification/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A small, practical verifier for **contraction-mapping smallness conditions**.

## What it checks

- **Core:** `gamma * (1 + t * c_P) <= eps`
- **Ledger:** `gamma_k * (1 + t_k * c_P) * exp(-sigma * delta_tau_k) <= eps` (for all k)
- **Coupled streams:** need `min{kappa1,kappa2} > 2*sqrt(eta1*eta2)`; prints `eps_eff = min - 2*sqrt(...)`

> In this tool, `eps` is the **threshold** on the left-hand side (LHS).  
> The verifier checks `LHS <= eps`. If your paper uses `1 - ε`, translate it or pass `--eps`.

---

## Quick start (Windows, Git Bash)

```bash
python -m venv .venv
source ./.venv/Scripts/activate
pip install -r requirements.txt

python src/verify_gaps.py examples/core_banach/example_core.json --type core_banach --verified
python src/verify_gaps.py examples/ledger/example_ledger.json --type ledger --verified
python src/verify_gaps.py examples/coupled_streams/example_coupled.json --type coupled_stream
Expected output: all OK.

CLI (abridged)
bash
Copy code
--type {core_banach,ledger,coupled_stream}
--eps <float>         # override threshold
--tol <float>         # numeric tolerance
--verified            # outward rounding guards (numpy.nextafter)
--interval            # planned: interval arithmetic
--use-gammaV          # planned: SVD-based ||R @ Gamma||_2
Repo layout
bash
Copy code
src/verify_gaps.py
examples/
.github/workflows/ci.yml
paper/            # optional
MIT licensed. See LICENSE.

bash
Copy code

### B) if you prefer terminal instead of web

```bash
# from repo root
notepad README.md             # paste the block above, save & close
git add README.md
git commit -m "README: clean markdown; remove stray instructions"
git push
