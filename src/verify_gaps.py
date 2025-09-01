#!/usr/bin/env python3
"""
Contraction-mapping verifier (threshold = eps).

Convention:
  - We compare LHS <= eps   (NOT 1-eps)
  - 'eps' is either provided via --eps, or computed from the JSON as:
        eps = alpha**beta * exp(-sigma * delta_tau_min)
  - All output uses plain ASCII (no Unicode) for Windows consoles.
"""

import json, math, argparse, sys, os
from typing import Any, Dict, List, Tuple

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def compute_eps(data: Dict[str,Any], override: float|None) -> float:
    if override is not None:
        return float(override)
    # Try common keys; fall back to 1.0 if missing
    alpha = data.get("alpha")
    beta  = data.get("beta")
    sigma = data.get("sigma")
    dtmin = data.get("delta_tau_min") or data.get("deltaTauMin")
    if alpha is not None and beta is not None and sigma is not None and dtmin is not None:
        return float(alpha)**float(beta) * math.exp(-float(sigma)*float(dtmin))
    # Try direct fields
    for k in ("eps","epsilon"):
        if k in data:
            return float(data[k])
    # Safe default
    return 1.0

def verify_core(data: Dict[str,Any], eps: float, cP: float, tol: float, verified: bool) -> bool:
    core = data.get("core_params", {})
    gamma = float(core.get("gamma", 0.5))
    t     = float(core.get("t", 0.1))
    lhs = gamma * (1.0 + t * cP)
    ok  = lhs <= eps + tol
    margin = eps - lhs
    print(f"Core Banach: {'OK' if ok else 'FAIL'} ({'margin' if ok else 'gap'} = {margin:+.3e})")
    return ok

def verify_ledger(data: Dict[str,Any], eps: float, cP: float, tol: float, verified: bool) -> bool:
    sigma = float(data.get("sigma", 0.0))
    steps = data.get("steps", [])
    if not steps:
        print("Ledger: no steps provided")
        return False
    all_ok = True
    worst_gap = -1e9
    for i,step in enumerate(steps):
        gamma = float(step.get("gamma", 0.5))
        t     = float(step.get("t", 0.1))
        dt    = float(step.get("delta_tau", data.get("delta_tau_min", 0.0)))
        lhs   = gamma * (1.0 + t * cP) * math.exp(-sigma * dt)
        ok    = lhs <= eps + tol
        margin = eps - lhs
        print(f"  step {i}: {'OK' if ok else 'FAIL'} ({'margin' if ok else 'gap'} = {margin:+.3e})")
        if not ok:
            all_ok = False
            worst_gap = max(worst_gap, -margin)  # positive if failing
    if all_ok:
        print("Ledger overall: OK")
    else:
        print(f"Ledger overall: FAIL (worst gap = {worst_gap:+.3e})")
    return all_ok

def verify_coupled(data: Dict[str,Any], tol: float) -> bool:
    sp = data.get("stream_params", {})
    k1 = float(sp.get("kappa1", 0.3))
    k2 = float(sp.get("kappa2", 0.4))
    e1 = float(sp.get("eta1",   0.1))
    e2 = float(sp.get("eta2",   0.1))
    min_k = min(k1, k2)
    coupling = 2.0 * math.sqrt(max(e1,0.0) * max(e2,0.0))
    eps_eff = min_k - coupling
    ok = eps_eff > tol
    print(f"Coupled streams: {'OK' if ok else 'FAIL'} (eps_eff = {eps_eff:.6g})")
    return ok

def main() -> int:
    ap = argparse.ArgumentParser(description="Verify contraction smallness conditions.")
    ap.add_argument("json_file", help="Path to JSON manifest")
    ap.add_argument("--type", dest="vtype",
                    choices=["core_banach","ledger","coupled_stream"],
                    required=True)
    ap.add_argument("--eps", type=float, default=None, help="Override eps threshold")
    ap.add_argument("--tol", type=float, default=1e-12, help="Numerical tolerance")
    ap.add_argument("--verified", action="store_true", help="Enable verified mode (placeholder)")
    ap.add_argument("--cP", type=float, default=None, help="Override c_P (operator norm of projection)")
    args = ap.parse_args()

    data = load_json(args.json_file)

    # threshold eps and projection norm
    eps = compute_eps(data, args.eps)
    cP  = float(args.cP) if args.cP is not None else float(data.get("c_P", 1.0))

    print(f"eps = {eps:.6g}   c_P = {cP}   type = {args.vtype}")

    if args.vtype == "core_banach":
        ok = verify_core(data, eps, cP, args.tol, args.verified)
    elif args.vtype == "ledger":
        ok = verify_ledger(data, eps, cP, args.tol, args.verified)
    else:  # coupled_stream
        ok = verify_coupled(data, args.tol)

    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
