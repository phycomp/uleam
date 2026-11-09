"""閉環迭代：調整權重 --> 測試 --> 驗收 (mantaro, polar)。"""

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

# Acceptance criteria
Z0_TOL = 1.0  # |Z0-50| <= 1
NEXT_TARGET = -40.0  # NEXT <= -40 dB
THERMAL_LIMIT = 500.0  # uW/ch

scenarios = [
    ("CF3", 3.4, 0.002, [{"material": "Cu", "thickness": 10.0}]),
    ("FPC", 3.2, 0.003, [{"material": "Cu", "thickness": 18.0}]),
    ("Uleam1", 3.5, 0.001, [{"material": "Ag", "thickness": 35.0}]),
]

print("=== ITERATION: per-scenario multi-objective optimization ===")
all_pass = True
results = []
for name, er, td, base_layers in scenarios:
    best = None
    for wi in range(10, 40):
        for hi in range(10, 40):
            for si in [20, 30, 40, 50, 60]:
                w = wi * 0.01
                h = hi * 0.01
                s = si * 0.01
                geo = opt.StriplineGeometry(
                    w=w, t=base_layers[0]["thickness"], h=h, s=s, L=100.0, n_channels=4
                )
                Z0 = opt.calc_stripline_impedance(geo, er)
                xt = opt.calc_crosstalk_stripline(geo, er, 1e9)
                boundary = opt.ThermalBoundary(T_hot=300.0, T_cold=0.01, stage="4K")
                ms = opt.MaterialStack(
                    layers=[
                        {
                            "material": base_layers[0]["material"],
                            "thickness": base_layers[0]["thickness"],
                            "width": w,
                        }
                    ]
                )
                th = opt.calc_thermal_load(geo, boundary, ms)
                # cost: Z0 error + crosstalk penalty + thermal penalty
                cost = (
                    abs(Z0 - 50.0)
                    + max(0, xt["NEXT_dB"] - NEXT_TARGET)
                    + max(0, th["per_channel_uW"] - THERMAL_LIMIT) / 1000.0
                )
                if best is None or cost < best[0]:
                    best = (cost, w, h, s, Z0, xt["NEXT_dB"], th["per_channel_uW"])
    cost, w, h, s, Z0, next_db, therm = best
    zok = bool(abs(Z0 - 50) <= Z0_TOL)
    nok = bool(next_db <= NEXT_TARGET)
    tok = bool(therm <= THERMAL_LIMIT)
    passed = bool(zok and nok and tok)
    all_pass = all_pass and passed
    results.append(
        {
            "name": name,
            "w": w,
            "h": h,
            "s": s,
            "Z0": round(Z0, 3),
            "NEXT": round(next_db, 2),
            "thermal": round(therm, 2),
            "Z0_ok": zok,
            "NEXT_ok": nok,
            "thermal_ok": tok,
            "PASS": passed,
        }
    )
    print(
        f"{name}: w={w:.2f} h={h:.2f} s={s:.2f} -> Z0={Z0:.2f} NEXT={next_db:.2f} therm={therm:.1f} | Z0_ok={zok} NEXT_ok={nok} therm_ok={tok} => {'PASS' if passed else 'FAIL'}"
    )

print("\nALL ACCEPTANCE PASS:", all_pass)
json.dump(
    {"iteration": "closed-loop", "results": results, "all_pass": all_pass},
    open(os.path.join(os.path.dirname(__file__), "acceptance.json"), "w"),
    indent=2,
    ensure_ascii=False,
)
print("Saved acceptance.json")
