# Contraction Mapping Verification

![CI](https://github.com/towre676-cloud/contraction-mapping-verification/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A small, practical verifier for **contraction-mapping smallness conditions**.

It checks inequalities of the form:

- **Core:** `gamma * (1 + t * c_P) <= eps_threshold`
- **Ledger (discrete):** `gamma_k * (1 + t_k * c_P) * exp(-sigma * delta_tau_k) <= eps_threshold` (for all steps)
- **Coupled streams:** requires `min{kappa1,kappa2} > 2*sqrt(eta1*eta2)`; it reports `eps_eff = min - 2*sqrt(...)`

> **Important:** In this tool, `eps` is the **threshold** on the left-hand side (LHS).  
> The verifier checks `LHS <= eps`. If your paper uses `1 - ε`, translate that to a threshold or pass `--eps` explicitly.

---

## Quick start (Windows, Git Bash)

1) Create & activate a venv
```bash
python -m venv .venv
source ./.venv/Scripts/activate
Install

bash
Copy code
pip install -r requirements.txt
Run the examples

bash
Copy code
python src/verify_gaps.py examples/core_banach/example_core.json --type core_banach --verified
python src/verify_gaps.py examples/ledger/example_ledger.json --type ledger --verified
python src/verify_gaps.py examples/coupled_streams/example_coupled.json --type coupled_stream
Expected output: all OK.

CLI (abridged)
--type {core_banach, ledger, coupled_stream}

--eps <float> override threshold

--tol <float> numeric tolerance

--verified outward-rounding guards (numpy.nextafter)

--interval (planned) interval arithmetic

--use-gammaV (planned) use SVD-based ||R @ Gamma||_2 bound

Repo layout
bash
Copy code
src/verify_gaps.py
examples/
.github/workflows/ci.yml
paper/            # optional
MIT licensed. See LICENSE.

yaml
Copy code

4. at the bottom, **Commit directly to `main`** → **Commit changes**.  
5. refresh the repo home page; the README should render with badges and code blocks.

---

## 2) Make sure CI is green
- click the **Actions** tab → open the latest **CI** run. You want green checkmarks.
- if nothing ran, trigger it with an empty commit:

```bash
git commit --allow-empty -m "ci: trigger"
git push
