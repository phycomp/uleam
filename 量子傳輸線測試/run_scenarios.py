"""量子傳輸線 測試情境：Mantaro 阻抗 + Polar + 串擾 + 熱負載，含優化 (權重調整後)。"""

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

# ---- Scenarios (原始 + 優化後) ----
scenarios = [
    (
        "CF3-stripline-50 (orig)",
        0.19,
        10.0,
        0.15,
        0.30,
        100.0,
        4,
        3.4,
        0.002,
        [{"material": "Cu", "thickness": 10.0, "width": 0.19}],
    ),
    (
        "FPC-micro-50 (orig)",
        0.12,
        18.0,
        0.10,
        0.20,
        50.0,
        8,
        3.2,
        0.003,
        [{"material": "Cu", "thickness": 18.0, "width": 0.12}],
    ),
    (
        "Uleam1-flex-50 (orig)",
        0.25,
        35.0,
        0.20,
        0.40,
        200.0,
        2,
        3.5,
        0.001,
        [{"material": "Ag", "thickness": 35.0, "width": 0.25}],
    ),
    # 優化後 (w=0.19, h=0.10)
    (
        "CF3-opt",
        0.19,
        10.0,
        0.10,
        0.30,
        100.0,
        4,
        3.4,
        0.002,
        [{"material": "Cu", "thickness": 10.0, "width": 0.19}],
    ),
    (
        "FPC-opt",
        0.19,
        18.0,
        0.10,
        0.20,
        50.0,
        8,
        3.2,
        0.003,
        [{"material": "Cu", "thickness": 18.0, "width": 0.19}],
    ),
    (
        "Uleam1-opt",
        0.19,
        35.0,
        0.10,
        0.40,
        200.0,
        2,
        3.5,
        0.001,
        [{"material": "Ag", "thickness": 35.0, "width": 0.19}],
    ),
]

results = []
for name, w, t, h, s, L, nch, er, td, layers in scenarios:
    geo = opt.StriplineGeometry(w=w, t=t, h=h, s=s, L=L, n_channels=nch)
    Z0 = opt.calc_stripline_impedance(geo, er)
    xt = opt.calc_crosstalk_stripline(geo, er, 1e9)
    boundary = opt.ThermalBoundary(T_hot=300.0, T_cold=0.01, stage="4K")
    ms = opt.MaterialStack(layers=layers)
    th = opt.calc_thermal_load(geo, boundary, ms)
    il = opt.calc_insertion_loss(geo, er, td, 1e9, "Cu")
    r = {
        "name": name,
        "Z0_ohm": round(float(Z0), 3),
        "Z0_err": round(float(Z0) - 50.0, 3),
        "NEXT_dB": round(float(xt["NEXT_dB"]), 2),
        "FEXT_dB": round(float(xt["FEXT_dB"]), 2),
        "thermal_uW": round(float(th["per_channel_uW"]), 3),
        "insertion_loss_dB": round(float(il), 4),
    }
    results.append(r)
    print(json.dumps(r, ensure_ascii=False))

print("\n=== ASSERTIONS ===")
ok = True
for r in results:
    zok = abs(r["Z0_err"]) < 5.0
    print(f"{r['name']}: Z0 within 5ohm? {zok} (err={r['Z0_err']})")
    ok = ok and zok
print("ALL Z0 OK:", ok)

# ---- Multi-objective optimization: minimize |Z0-50| + |NEXT+60| + thermal/1000 ----
print("\n=== MULTI-OBJECTIVE OPTIMIZATION (grid search) ===")
best = None
for wi in range(10, 40):
    for hi in range(10, 40):
        for si in [20, 30, 40]:
            w = wi * 0.01
            h = hi * 0.01
            s = si * 0.01
            geo = opt.StriplineGeometry(w=w, t=10.0, h=h, s=s, L=100.0, n_channels=4)
            Z0 = opt.calc_stripline_impedance(geo, 3.4)
            xt = opt.calc_crosstalk_stripline(geo, 3.4, 1e9)
            boundary = opt.ThermalBoundary(T_hot=300.0, T_cold=0.01, stage="4K")
            ms = opt.MaterialStack(
                layers=[{"material": "Cu", "thickness": 10.0, "width": w}]
            )
            th = opt.calc_thermal_load(geo, boundary, ms)
            cost = (
                abs(Z0 - 50.0) + abs(xt["NEXT_dB"] + 60) + th["per_channel_uW"] / 1000.0
            )
            if best is None or cost < best[0]:
                best = (cost, w, h, s, Z0, xt["NEXT_dB"], th["per_channel_uW"])
print(
    "best cost=%.3f w=%.2fmm h=%.2fmm s=%.2fmm Z0=%.2f NEXT=%.2f dB thermal=%.2fuW"
    % best
)

out = {
    "scenarios": results,
    "optimization": {
        "cost": best[0],
        "w_mm": best[1],
        "h_mm": best[2],
        "s_mm": best[3],
        "Z0": best[4],
        "NEXT_dB": best[5],
        "thermal_uW": best[6],
    },
}
json.dump(
    out,
    open(os.path.join(os.path.dirname(__file__), "results.json"), "w"),
    indent=2,
    ensure_ascii=False,
)
print("\nSaved results.json")
