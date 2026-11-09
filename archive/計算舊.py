# =====================================================================
# 1. 確定性物理核心引擎 (Deterministic Physics Engine)
# =====================================================================

def calculate_london_penetration(material: str, temp: float) -> float:
    """計算超導體在特定溫度下的 London 穿透深度 (單位: nm)"""
    tc_map = {"NbTi": 9.2, "Al": 1.2, "Nb": 9.2}
    lambda_0_map = {"NbTi": 240.0, "Al": 50.0, "Nb": 40.0} # 0K 時的穿透深度
    
    tc = tc_map.get(material, 9.2)
    lambda_0 = lambda_0_map.get(material, 240.0)
    
    if temp >= tc:
        return 0.0
    # 依據 Gorter-Casimir 二流體模型
    return lambda_0 / sqrt(1 - (temp / tc) ** 4)

def calculate_kinetic_inductance(w_mil: float, t_mil: float, lambda_nm: float) -> float:
    """依據幾何截面與穿透深度估算動態電感 Lk (單位: nH/m)"""
    if lambda_nm == 0:
        return 0.0
    w_m = w_mil * 2.54e-5
    t_m = t_mil * 2.54e-5
    lambda_m = lambda_nm * 1e-9
    
    # 簡化薄膜近似公式: Lk = (mu_0 * lambda^2) / (w * t)
    mu_0 = 4 * pi * 1e-7
    lk = (mu_0 * (lambda_m ** 2)) / (w_m * t_m)
    return lk * 1e9 # 轉為 nH/m

def calculate_quantum_impedance(width_mil: float, thickness_mil: float, h_mil: float, er: float, material: str, temp: float) -> dict:
    """含超導修正的 Wheeler/Hammerstad 阻抗計算"""
    # 幾何基礎電感與電容近似計算 (50歐姆常溫基礎)
    w_h = width_mil / h_mil
    # 簡易 Microstrip 幾何阻抗公式
    if w_h <= 1:
        eeff = (er + 1) / 2 + ((er - 1) / 2) * ((1 + 12 / w_h)**(-0.5) + 0.04 * (1 - w_h)**2)
        zo_geo = (60 / sqrt(eeff)) * log(8 / w_h + 0.25 * w_h)
    else:
        eeff = (er + 1) / 2 + ((er - 1) / 2) * (1 + 12 / w_h)**(-0.5)
        zo_geo = (120 * pi) / (sqrt(eeff) * (w_h + 1.393 + 0.667 * log(w_h + 1.444)))
        
    c_geo = 3.333e-9 * sqrt(eeff) / zo_geo # F/m
    l_geo = zo_geo**2 * c_geo # H/m
    
    # 超導決策分支
    tc_map = {"NbTi": 9.2, "Al": 1.2, "Nb": 9.2}
    is_sc = material in tc_map and temp < tc_map[material]
    
    if is_sc:
        lambda_nm = calculate_london_penetration(material, temp)
        lk_nh_m = calculate_kinetic_inductance(width_mil, thickness_mil, lambda_nm)
        l_total = (l_geo * 1e9) + lk_nh_m # 統一單位 nH/m
        zo_final = sqrt((l_total * 1e-9) / c_geo)
    else:
        zo_final = zo_geo
        lk_nh_m = 0.0
        
    return {
        "zo": round(zo_final, 2),
        "is_superconducting": is_sc,
        "kinetic_inductance_nh_m": round(lk_nh_m, 2),
        "loss_db_per_m": 0.0 if is_sc else round(0.5 * sqrt(temp + 1), 3)
    }

def calculate_coupled_thermal_load(current_stackup: dict, stages: list) -> dict:
    """非線性固體熱傳導積分與微波衰減器自發熱動態耦合計算"""
    total_solid = 0.0
    total_attenuator = 0.0
    
    # 簡化不同材料低溫熱導率積分常數
    # k(T) = a * T^b
    material_props = {
        "Cu": {"a": 0.1, "b": 1.0},       # 高熱導
        "NbTi": {"a": 0.0005, "b": 1.5},  # 極低熱導 (超導態)
        "Nb": {"a": 0.002, "b": 1.3}
    }
    
    mat = current_stackup["material"]
    p = material_props.get(mat, material_props["NbTi"])
    
    # 假設從常溫段到 10mK 的逐級傅立葉熱傳導
    for i in range(len(stages) - 1):
        t_high = stages[i]["temp_k"]
        t_low = stages[i+1]["temp_k"]
        length = stages[i]["line_length_m"]
        
        # 傅立葉積分: Q = (A / L) * 積分[k(T)dT]
        area = (current_stackup["width_mil"] * current_stackup["thickness_mil"]) * 6.4516e-10 # m^2
        k_integral = (p["a"] / (p["b"] + 1)) * (t_high**(p["b"]+1) - t_low**(p["b"]+1))
        solid_heat = (area / length) * k_integral
        total_solid += solid_heat
        
        # 衰減器自發熱 (Attenuator Dissipation) 耦合
        # 訊號衰減帶來的局部功率釋放
        att_db = stages[i]["attenuation_db"]
        if att_db > 0:
            input_power_w = 1e-6 # 假設微波輸入輸入 -30 dBm = 1微瓦
            rf_heat = input_power_w * (1 - 10**(-att_db / 10))
            total_attenuator += rf_heat

    total_load = total_solid + total_attenuator
    return {
        "total_load_w": total_load,
        "solid_conduction_w": total_solid,
        "attenuator_dissipation_w": total_attenuator
    }


