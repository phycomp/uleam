import numpy as np
import math

def calc_microstrip_qubit(W, H, T, Er, freq_ghz):
    """4-12 GHz 微波微帶線快速阻抗與介質損耗估算（IPC-2141 逼近）"""
    ln_term = math.log(5.98 * H / (0.8 * W + T))
    Z0 = (87 / math.sqrt(Er + 1.41)) * ln_term
    loss_factor = 0.0027 if Er < 4 else 0.0001
    alpha_d = 0.0912 * freq_ghz * math.sqrt(Er) * loss_factor  # dB/cm
    return round(Z0, 2), round(alpha_d, 4)

# =====================================================================
# 1. 確定性物理核心引擎 (不變，保持精準物理計算)
# =====================================================================

def calculate_london_penetration(material: str, temp: float) -> float:
    tc_map = {"NbTi": 9.2, "Al": 1.2, "Nb": 9.2}
    lambda_0_map = {"NbTi": 240.0, "Al": 50.0, "Nb": 40.0}
    tc = tc_map.get(material, 9.2)
    lambda_0 = lambda_0_map.get(material, 240.0)
    if temp >= tc: return 0.0
    return lambda_0 / np.sqrt(1 - (temp / tc) ** 4)

def calculate_kinetic_inductance(w_mil: float, t_mil: float, lambda_nm: float) -> float:
    if lambda_nm == 0: return 0.0
    w_m = w_mil * 2.54e-5
    t_m = t_mil * 2.54e-5
    lambda_m = lambda_nm * 1e-9
    mu_0 = 4 * np.pi * 1e-7
    return ((mu_0 * (lambda_m ** 2)) / (w_m * t_m)) * 1e9

def calculate_quantum_impedance(width_mil: float, thickness_mil: float, h_mil: float, er: float, material: str, temp: float) -> dict:
    if width_mil <= 0 or h_mil <= 0: return {"zo": 999, "is_superconducting": False, "kinetic_inductance_nh_m": 0, "loss_db_per_m": 999}
    w_h = width_mil / h_mil
    if w_h <= 1:
        eeff = (er + 1) / 2 + ((er - 1) / 2) * ((1 + 12 / w_h)**(-0.5) + 0.04 * (1 - w_h)**2)
        zo_geo = (60 / np.sqrt(eeff)) * np.log(8 / w_h + 0.25 * w_h)
    else:
        eeff = (er + 1) / 2 + ((er - 1) / 2) * (1 + 12 / w_h)**(-0.5)
        zo_geo = (120 * np.pi) / (np.sqrt(eeff) * (w_h + 1.393 + 0.667 * np.log(w_h + 1.444)))
    c_geo = 3.333e-9 * np.sqrt(eeff) / zo_geo
    l_geo = zo_geo**2 * c_geo
    tc_map = {"NbTi": 9.2, "Al": 1.2, "Nb": 9.2}
    is_sc = material in tc_map and temp < tc_map[material]
    if is_sc:
        lambda_nm = calculate_london_penetration(material, temp)
        lk_nh_m = calculate_kinetic_inductance(width_mil, thickness_mil, lambda_nm)
        l_total = (l_geo * 1e9) + lk_nh_m
        zo_final = np.sqrt((l_total * 1e-9) / c_geo)
    else:
        zo_final = zo_geo
        lk_nh_m = 0.0
    return {
        "zo": round(zo_final, 2), "is_superconducting": is_sc,
        "kinetic_inductance_nh_m": round(lk_nh_m, 2),
        "loss_db_per_m": 0.0 if is_sc else round(0.5 * np.sqrt(temp + 1), 3)
    }

def calculate_coupled_thermal_load(current_stackup: dict, stages: list) -> dict:
    total_solid = 0.0
    total_attenuator = 0.0
    material_props = {
        "Cu": {"a": 0.1, "b": 1.0}, "NbTi": {"a": 0.0005, "b": 1.5}, "Nb": {"a": 0.002, "b": 1.3}
    }
    mat = current_stackup["material"]
    p = material_props.get(mat, material_props["NbTi"])
    for i in range(len(stages) - 1):
        t_high = stages[i]["temp_k"]
        t_low = stages[i+1]["temp_k"]
        length = stages[i]["line_length_m"]
        area = (current_stackup["width_mil"] * current_stackup["thickness_mil"]) * 6.4516e-10
        k_integral = (p["a"] / (p["b"] + 1)) * (t_high**(p["b"]+1) - t_low**(p["b"]+1))
        total_solid += (area / length) * k_integral
        att_db = stages[i]["attenuation_db"]
        if att_db > 0:
            total_attenuator += 1e-6 * (1 - 10**(-att_db / 10))
    return {"total_load_w": total_solid + total_attenuator, "solid_conduction_w": total_solid, "attenuation_db_per_m": total_attenuator}
