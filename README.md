
# Contraction Mapping Verification

A practical, reproducible framework for checking contraction-mapping smallness conditions with:
- Interval arithmetic (outward rounding)
- Verified comparisons (`nextafter` guards)
- Spectral helpers (power iteration, SVD) incl. sharper `γ_V = ||RΓ||_2`

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
python src/verify_gaps.py examples/core_banach/example_core.json --type core_banach
python src/verify_gaps.py examples/ledger/example_ledger.json --type ledger --interval --verified
python src/verify_gaps.py examples/coupled_streams/example_coupled.json --type coupled_stream
python src/verify_gaps.py examples/gamma_v/example_gammaV.json --type gammaV --use-gammaV --svd-exact
```

See `docs/usage.md` for full CLI.
