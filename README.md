# Contraction Mapping Verification

Run locally (Windows, Git Bash):

```bash
python -m venv .venv
source ./.venv/Scripts/activate
pip install -r requirements.txt

python src/verify_gaps.py examples/core_banach/example_core.json --type core_banach --verified
python src/verify_gaps.py examples/ledger/example_ledger.json --type ledger --verified
python src/verify_gaps.py examples/coupled_streams/example_coupled.json --type coupled_stream
