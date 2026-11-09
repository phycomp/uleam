# 儲存為 agent_core.py
import sys
import json
import numpy as np
import pandas as pd

# [這裡保持與之前相同的核心物理函數：
from 計算 import calculate_london_penetration, calculate_quantum_impedance, calculate_coupled_thermal_load
# (為節省篇幅，此處省略與 V2 相同的物理公式函數，實際布署時請完整複製過來)

def run_optimization_workflow(input_spec):
    """專門供背景與定時任務執行的優化工作流"""
    target_zo = input_spec["target_zo"]
    thermal_budget_uw = input_spec["thermal_budget_uw"]
    min_h_mil = input_spec["min_h_mil"]
    er_dielectric = input_spec["er_dielectric"]
    
    stages = [
        {"stage_name": "Room Temp", "temp_k": 300.0, "line_length_m": 0.5, "attenuation_db": 0},
        {"stage_name": "4K Stage", "temp_k": 4.2, "line_length_m": 0.3, "attenuation_db": 10},
        {"stage_name": "Still", "temp_k": 0.8, "line_length_m": 0.1, "attenuation_db": 10},
        {"stage_name": "MC Stage", "temp_k": 0.01, "line_length_m": 0.1, "attenuation_db": 20}
    ]
    
    seeds = [
        {"name": "種子 A (傳統銅基)", "material": "Cu", "width_mil": 12.0, "thickness_mil": 1.4, "h_mil": 8.0},
        {"name": "種子 B (超導微型)", "material": "NbTi", "width_mil": 6.0, "thickness_mil": 0.5, "h_mil": 4.0},
        {"name": "種子 C (高阻抗高介質)", "material": "Nb", "width_mil": 16.0, "thickness_mil": 1.0, "h_mil": 10.0}
    ]
    
    solution_pool = []
    zo_tolerance = 1.0
    
    for iter_idx in range(1, 11):
        for seed in seeds:
            elec_res = calculate_quantum_impedance(seed["width_mil"], seed["thickness_mil"], seed["h_mil"], er_dielectric, seed["material"], temp=0.01)
            thermal_res = calculate_coupled_thermal_load(seed, stages)
            
            zo_actual = elec_res["zo"]
            heat_uw = thermal_res["total_load_w"] * 1e6
            
            is_zo_ok = abs(zo_actual - target_zo) <= zo_tolerance
            is_thermal_ok = heat_uw <= thermal_budget_uw
            
            if is_zo_ok:
                tag = "超導冷量最優" if is_thermal_ok else "退相干保障（熱耗略高）"
                solution_pool.append({
                    "tag": f"{seed['name']}-{tag}", "material": seed["material"],
                    "width_mil": round(seed["width_mil"], 2), "h_mil": round(seed["h_mil"], 2),
                    "zo": zo_actual, "heat_uw": round(heat_uw, 4)
                })
            
            # 敏感度微調邏輯 (與 V2 相同)
            delta = 0.1
            e_up = calculate_quantum_impedance(seed["width_mil"] + delta, seed["thickness_mil"], seed["h_mil"], er_dielectric, seed["material"], temp=0.01)
            dZo_dW = (e_up["zo"] - zo_actual) / delta
            e_h_up = calculate_quantum_impedance(seed["width_mil"], seed["thickness_mil"], seed["h_mil"] + delta, er_dielectric, seed["material"], temp=0.01)
            dZo_dH = (e_h_up["zo"] - zo_actual) / delta
            
            if not is_zo_ok or not is_thermal_ok:
                if seed["material"] == "Cu" and heat_uw > thermal_budget_uw:
                    seed["material"] = "NbTi"
                else:
                    zo_error = target_zo - zo_actual
                    step_w = -0.8 if heat_uw > thermal_budget_uw and seed["width_mil"] > min_h_mil else np.clip(zo_error / (dZo_dW + 1e-5), -1.0, 1.0)
                    step_h = np.clip((zo_error - dZo_dW * step_w) / (dZo_dH + 1e-5), -1.5, 1.5)
                    seed["width_mil"] = max(2.0, seed["width_mil"] + step_w)
                    seed["h_mil"] = max(min_h_mil, seed["h_mil"] + step_h)
                    
        if iter_idx == 5 and len(solution_pool) == 0:
            zo_tolerance = 2.0

    # 挑選最佳三套輸出
    df_all = pd.DataFrame(solution_pool).drop_duplicates(subset=["material", "width_mil", "zo"])
    df_all["zo_dev"] = (df_all["zo"] - target_zo).abs()
    df_final = df_all.sort_values(by=["zo_dev", "heat_uw"]).head(3).reset_index(drop=True)
    
    return df_final.to_dict(orient="records")

if __name__ == "__main__":
    # 從命令列讀取傳入的 Spec JSON
    try:
        input_data = json.loads(sys.argv[1])
    except:
        # 預設測試值
        input_data = {"target_zo": 50.0, "thermal_budget_uw": 1.0, "min_h_mil": 4.0, "er_dielectric": 4.2}
        
    results = run_optimization_workflow(input_data)
    
    # 正式環境通常會將結果寫入資料庫或發送 API，這裡先標準輸出 JSON
    print(json.dumps(results, indent=4, ensure_ascii=False))
    # 使用範例 python3 agent_production.py '{"target_zo": 50.0, "thermal_budget_uw": 0.5, "min_h_mil": 4.0, "er_dielectric": 10.0}'
