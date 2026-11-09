"""最終驗收：所有情境 (含 NbTi) 通過 Z0/NEXT/thermal。"""

import sys, os, types, json

scipy = types.ModuleType("scipy")
scipy.optimize = types.ModuleType("scipy.optimize")
sys.modules["scipy"] = scipy
sys.modules["scipy.optimize"] = scipy.optimize
scipy.optimize.minimize = lambda *a, **k: None
scipy.optimize.differential_evolution = lambda *a, **k: None
scipy.optimize.NonlinearConstraint = lambda *a, **k: None

UTIL = "/home/sam/量傳線/德夫/約束優化Util.py"
src = (
    open(UTIL)
    .read()
    .replace(
        "from scipy.optimize import minimize, differential_evolution, NonlinearConstraint\n",
        "",
    )
)
ns = {}
exec(compile(src, UTIL, "exec"), ns)
opt = types.SimpleNamespace(**{k: ns[k] for k in ns if not k.startswith("__")})

Z0_TOL = 1.0
NEXT_TARGET = -40.0
THERMAL_LIMIT = 500.0

# Final accepted designs (from closed-loop optimization)
designs = [
    ("CF3 (Cu)", 3.4, 0.002, "Cu", 10.0, 0.25, 0.13, 0.50),
    ("FPC (Cu)", 3.2, 0.003, "Cu", 10.0, 0.30, 0.15, 0.60),
    ("Uleam1 (NbTi)", 3.5, 0.001, "NbTi", 35.0, 0.24, 0.14, 0.50),
]

print("=== FINAL ACCEPTANCE ===")
all_pass = True
results = []
for name, er, td, mat, t, w, h, s in designs:
    geo = opt.StriplineGeometry(w=w, t=t, h=h, s=s, L=100.0, n_channels=4)
    Z0 = opt.calc_stripline_impedance(geo, er)
    xt = opt.calc_crosstalk_stripline(geo, er, 1e9)
    boundary = opt.ThermalBoundary(T_hot=300.0, T_cold=0.01, stage="4K")
    ms = opt.MaterialStack(layers=[{"material": mat, "thickness": t, "width": w}])
    th = opt.calc_thermal_load(geo, boundary, ms)
    zok = bool(abs(Z0 - 50) <= Z0_TOL)
    nok = bool(xt["NEXT_dB"] <= NEXT_TARGET)
    tok = bool(th["per_channel_uW"] <= THERMAL_LIMIT)
    passed = bool(zok and nok and tok)
    all_pass = all_pass and passed
    results.append(
        {
            "name": name,
            "material": mat,
            "w": w,
            "h": h,
            "s": s,
            "t_um": t,
            "Z0": round(float(Z0), 3),
            "NEXT": round(float(xt["NEXT_dB"]), 2),
            "thermal": round(float(th["per_channel_uW"]), 2),
            "Z0_ok": zok,
            "NEXT_ok": nok,
            "thermal_ok": tok,
            "PASS": passed,
        }
    )
    print(
        f"{name}: w={w:.2f} h={h:.2f} s={s:.2f} t={t} -> Z0={Z0:.2f} NEXT={xt['NEXT_dB']:.2f} therm={th['per_channel_uW']:.1f} | Z0_ok={zok} NEXT_ok={nok} therm_ok={tok} => {'PASS' if passed else 'FAIL'}"
    )

print("\nALL ACCEPTANCE PASS:", all_pass)
json.dump(
    {"final_acceptance": True, "all_pass": all_pass, "results": results},
    open(os.path.join(os.path.dirname(__file__), "acceptance_final.json"), "w"),
    indent=2,
    ensure_ascii=False,
)
print("Saved acceptance_final.json")
