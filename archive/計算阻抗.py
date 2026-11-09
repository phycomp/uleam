from numpy import sqrt
## 2. 確定性物理工具箱 (Deterministic Tools)
# LLM（如 Claude 或 GPT）只負責調整幾何參數與切換材料，所有的物理公式必須寫死在 Python Functions 中。
## 🔧 工具 A：超導阻抗與損耗計算器 (electrical_solver)

# * 邏輯：接收幾何尺寸，若材料為超導體（如 NbTi、Al），自動啟用 London Penetration Depth $\lambda_L$ 與動態電感 $L_k$ 修正公式，覆蓋常溫 Wheeler/Hammerstad 公式。

import numpy as np
def calculate_quantum_impedance(width: float, thickness: float, h: float, er: float, material: str, temp: float) -> dict:
    # 1. 基礎 Wheeler/Hammerstad 常溫解析幾何阻抗計算
    zo_geometric = standard_wheeler_formula(width, thickness, h, er)
    
    # 2. 決策分支：檢查是否觸發超導修正
    if material in ["NbTi", "Al", "Nb"] and temp < 9.2:  # 假設 NbTi Tc ~ 9.2K
        # 計算 London 穿透深度與動態電感 Lk
        lambda_l = calculate_london_penetration(material, temp)
        kinetic_inductance = calculate_kinetic_inductance(width, thickness, lambda_l)
        
        # 修正阻抗 Zo = sqrt((L_geometric + L_kinetic) / C)
        zo_final = zo_geometric * sqrt(1 + (kinetic_inductance / standard_inductance(width, h)))
        is_superconducting = True
    else:
        zo_final = zo_geometric
        is_superconducting = False
        
    return {
        "zo": zo_final,
        "is_superconducting": is_superconducting,
        "attenuation_db_per_m": 0.0 if is_superconducting else estimate_copper_loss(temp)
    }

## 🔧 工具 B：熱負載與衰減器自發熱耦合計算器 (thermal_coupled_solver)

# * 邏輯：進行傅立葉定律的非線性積分（熱導率 $\kappa(T) = a \cdot T^b$），並疊加微波訊號通過衰減器（Attenuator）時轉換成的熱能（Attenuator Dissipation）。

def calculate_coupled_thermal_load(stackup: List[dict], stages: List[dict]) -> dict:
    total_solid_conduction = 0.0
    total_attenuator_dissipation = 0.0
    
    for stage in stages:
        # 1. 固體熱傳導積分 (傅立葉定律)
        kappa_t = get_material_thermal_conductivity(stackup, stage['temp_k'])
        solid_heat = integrate_fourier(kappa_t, stage['line_length_m'])
        total_solid_conduction += solid_heat
        
        # 2. 微波噪聲衰減器自發熱計算 (Attenuator Dissipation)
        # 訊號功率與衰減量產生的局部熱能
        rf_heat = calculate_attenuator_heat(stage['attenuation_db'], input_power_dbm=-30) 
        total_attenuator_dissipation += rf_heat
        
    return {
        "total_load_w": total_solid_conduction + total_attenuator_dissipation,
        "solid_conduction_w": total_solid_conduction,
        "attenuator_dissipation_w": total_attenuator_dissipation
    }
