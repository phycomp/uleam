"""閉環迭代2：含厚度/材料優化，目標全部驗收通過。"""

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

# (name, er, tan_delta, material, thickness_options)
scenarios = [
    ("CF3", 3.4, 0.002, "Cu", [10.0, 18.0]),
    ("FPC", 3.2, 0.003, "Cu", [10.0, 18.0]),
    ("Uleam1", 3.5, 0.001, "Ag", [35.0]),
    # try NbTi for Uleam1 (superconducting, lower thermal)
    ("Uleam1-NbTi", 3.5, 0.001, "NbTi", [35.0]),
]

print("=== ITERATION 2: thickness + material optimization ===")
all_pass = True
results = []
for name, er, td, mat, t_opts in scenarios:
    best = None
    for t in t_opts:
        for wi in range(10, 40):
            for hi in range(10, 40):
                for si in [30, 40, 50, 60]:
                    w = wi * 0.01
                    h = hi * 0.01
                    s = si * 0.01
                    geo = opt.StriplineGeometry(
                        w=w, t=t, h=h, s=s, L=100.0, n_channels=4
                    )
                    Z0 = opt.calc_stripline_impedance(geo, er)
                    xt = opt.calc_crosstalk_stripline(geo, er, 1e9)
                    boundary = opt.ThermalBoundary(T_hot=300.0, T_cold=0.01, stage="4K")
                    ms = opt.MaterialStack(
                        layers=[{"material": mat, "thickness": t, "width": w}]
                    )
                    th = opt.calc_thermal_load(geo, boundary, ms)
                    cost = (
                        abs(Z0 - 50.0)
                        + max(0, xt["NEXT_dB"] - NEXT_TARGET)
                        + max(0, th["per_channel_uW"] - THERMAL_LIMIT) / 500.0
                    )
                    if best is None or cost < best[0]:
                        best = (
                            cost,
                            w,
                            h,
                            s,
                            t,
                            mat,
                            Z0,
                            xt["NEXT_dB"],
                            th["per_channel_uW"],
                        )
    cost, w, h, s, t, mat, Z0, next_db, therm = best
    zok = bool(abs(Z0 - 50) <= Z0_TOL)
    nok = bool(next_db <= NEXT_TARGET)
    tok = bool(therm <= THERMAL_LIMIT)
    passed = bool(zok and nok and tok)
    all_pass = all_pass and passed
    results.append(
        {
            "name": name,
            "material": mat,
            "t_um": t,
            "w": w,
            "h": h,
            "s": s,
            "Z0": round(float(Z0), 3),
            "NEXT": round(float(next_db), 2),
            "thermal": round(float(therm), 2),
            "Z0_ok": zok,
            "NEXT_ok": nok,
            "thermal_ok": tok,
            "PASS": passed,
        }
    )
    print(
        f"{name} ({mat}): t={t} w={w:.2f} h={h:.2f} s={s:.2f} -> Z0={Z0:.2f} NEXT={next_db:.2f} therm={therm:.1f} | Z0_ok={zok} NEXT_ok={nok} therm_ok={tok} => {'PASS' if passed else 'FAIL'}"
    )

print("\nALL ACCEPTANCE PASS:", all_pass)
json.dump(
    {"iteration": "closed-loop-2", "results": results, "all_pass": all_pass},
    open(os.path.join(os.path.dirname(__file__), "acceptance2.json"), "w"),
    indent=2,
    ensure_ascii=False,
)
print("Saved acceptance2.json")
