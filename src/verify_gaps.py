#!/usr/bin/env python3
"""
Verifier for contraction-mapping smallness conditions.
- Core Banach:      gamma * (1 + t * c_P) <= 1 - eps
- Ledger (per step):gamma_k * (1 + t_k * c_P) * exp(-sigma * delta_tau_k) <= 1 - eps
- Coupled streams:  min{kappa1,kappa2} > 2*sqrt(eta1*eta2), eps = min - 2sqrt
Extras:
- --interval: outward rounding using simple intervals
- --verified: use nextafter to make <= comparisons safe in float
- --create-example: write a sample JSON manifest
"""
import argparse, json, math, sys
from math import sqrt
from typing import Tuple, Dict, Any
import numpy as np

# ---------- verified numeric helpers ----------
def le_verified(a: float, b: float) -> bool:
    """Return True if a <= b allowing for ulp-level rounding using nextafter."""
    a2 = np.nextafter(a, -np.inf)  # round a down
    b2 = np.nextafter(b, +np.inf)  # round b up
    return a2 <= b2

def outward_mul(a: Tuple[float,float], b: Tuple[float,float]) -> Tuple[float,float]:
    (al, au), (bl, bu) = a, b
    cands = [al*bl, al*bu, au*bl, au*bu]
    return (math.nextafter(min(cands), -math.inf),
            math.nextafter(max(cands), +math.inf))

def outward_add(a: Tuple[float,float], b: Tuple[float,float]) -> Tuple[float,float]:
    (al, au), (bl, bu) = a, b
    return (math.nextafter(al+bl, -math.inf),
            math.nextafter(au+bu, +math.inf))

def outward_exp(x: Tuple[float,float]) -> Tuple[float,float]:
    xl, xu = x
    lo = math.nextafter(math.exp(xl), -math.inf)
    hi = math.nextafter(math.exp(xu), +math.inf)
    return (lo, hi)

# ---------- core checks ----------
def core_banach_ok(d: Dict[str,Any], eps: float, cP: float,
                   use_interval: bool, verified: bool) -> Tuple[bool, float]:
    gamma = float(d["core_params"]["gamma"])
    t = float(d["core_params"]["t"])
    if use_interval:
        lhs = outward_mul((gamma,gamma), outward_add((1.0,1.0), (t*cP, t*cP)))
        rhs = (1.0 - eps, 1.0 - eps)
        ok = lhs[1] <= rhs[0]   # worst upper <= best lower
        lhs_num = lhs[1]; rhs_num = rhs[0]
    else:
        lhs_num = gamma * (1.0 + t * cP)
        rhs_num = 1.0 - eps
        ok = le_verified(lhs_num, rhs_num) if verified else (lhs_num <= rhs_num)
    return ok, lhs_num - rhs_num

def ledger_ok(d: Dict[str,Any], eps: float, cP: float,
              sigma: float, use_interval: bool, verified: bool) -> Tuple[bool, float]:
    worst_gap = -1e9
    ok_all = True
    for i, step in enumerate(d.get("steps", [])):
        g = float(step["gamma"]); t = float(step["t"]); dt = float(step["delta_tau"])
        if use_interval:
            lhs = outward_mul((g,g), outward_add((1.0,1.0), (t*cP, t*cP)))
            decay = outward_exp((-sigma*dt, -sigma*dt))
            lhs = outward_mul(lhs, decay)
            rhs = (1.0 - eps, 1.0 - eps)
            ok = lhs[1] <= rhs[0]
            gap = lhs[1] - rhs[0]
        else:
            lhs_num = g * (1.0 + t * cP) * math.exp(-sigma * dt)
            rhs_num = 1.0 - eps
            ok = le_verified(lhs_num, rhs_num) if verified else (lhs_num <= rhs_num)
            gap = lhs_num - rhs_num
        worst_gap = max(worst_gap, gap)
        if not ok:
            ok_all = False
        print(f"  step {i}: {'OK ' if ok else 'FAIL'} (gap = {gap:+.3e})")
    return ok_all, worst_gap

def coupled_ok(d: Dict[str,Any]) -> Tuple[bool, float]:
    sp = d["stream_params"]
    k1 = float(sp["kappa1"]); k2 = float(sp["kappa2"])
    e1 = float(sp["eta1"]);   e2 = float(sp["eta2"])
    coupling = 2.0 * sqrt(max(e1,0.0) * max(e2,0.0))
    m = min(k1, k2)
    ok = (m > coupling)
    eps_eff = m - coupling if ok else 0.0
    return ok, eps_eff

# ---------- eps from witness parameters ----------
def compute_eps(d: Dict[str,Any]) -> float:
    alpha = float(d.get("alpha", 0.99))
    beta  = float(d.get("beta",  1.0))
    sigma = float(d.get("sigma", 1.0))
    dtmin = float(d.get("delta_tau_min", 0.1))
    return (alpha ** beta) * math.exp(-sigma * dtmin)

# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="Contraction smallness verifier")
    ap.add_argument("json", nargs="?", help="manifest JSON file")
    ap.add_argument("--type", choices=["core_banach","ledger","coupled_stream"], default="core_banach")
    ap.add_argument("--eps", type=float, default=None, help="override epsilon")
    ap.add_argument("--cP", type=float, default=1.0, help="||P||_op")
    ap.add_argument("--interval", action="store_true", help="use outward rounding intervals")
    ap.add_argument("--verified", action="store_true", help="nextafter guard on comparisons")
    ap.add_argument("--create-example", choices=["core","ledger","coupled"], help="write example JSON to stdout")
    args = ap.parse_args()

    if args.create_example:
        if args.create_example == "core":
            ex = {"alpha":0.9982,"beta":0.0021,"sigma":0.12,"delta_tau_min":0.0047,
                  "c_P":1.0,"verification_type":"core_banach",
                  "core_params":{"gamma":0.6,"t":0.1}}
        elif args.create_example == "ledger":
            ex = {"alpha":0.9982,"beta":0.0021,"sigma":0.12,"delta_tau_min":0.0047,
                  "c_P":1.0,"verification_type":"ledger",
                  "steps":[
                      {"gamma":0.993,"t":0.01,"delta_tau":0.005},
                      {"gamma":0.992,"t":0.015,"delta_tau":0.0048},
                      {"gamma":0.994,"t":0.012,"delta_tau":0.0052}
                  ]}
        else:
            ex = {"verification_type":"coupled_stream",
                  "stream_params":{"kappa1":0.3,"kappa2":0.28,"eta1":0.04,"eta2":0.025}}
        print(json.dumps(ex, indent=2))
        return 0

    if not args.json:
        print("error: provide a manifest JSON or --create-example", file=sys.stderr)
        return 2

    with open(args.json,"r") as f:
        data = json.load(f)

    eps = args.eps if args.eps is not None else compute_eps(data)
    cP  = float(data.get("c_P", args.cP))
    sigma = float(data.get("sigma", 1.0))

    print(f"eps = {eps:.6g}   c_P = {cP}   type = {args.type}")

    if args.type == "core_banach":
        ok, gap = core_banach_ok(data, eps, cP, args.interval, args.verified)
        print(f"Core Banach: {'OK' if ok else 'FAIL'} (gap = {gap:+.3e})")
        return 0 if ok else 1

    if args.type == "ledger":
        ok, worst = ledger_ok(data, eps, cP, sigma, args.interval, args.verified)
        print(f"Ledger overall: {'OK' if ok else 'FAIL'} (worst gap = {worst:+.3e})")
        return 0 if ok else 1

    if args.type == "coupled_stream":
        ok, eps_eff = coupled_ok(data)
        print(f"Coupled streams: {'OK' if ok else 'FAIL'} (eps_eff = {eps_eff:.6g})")
        return 0 if ok else 1

    print("unknown type")
    return 2

if __name__ == "__main__":
    sys.exit(main())
