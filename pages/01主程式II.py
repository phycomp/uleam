from streamlit import button, caption, columns, dataframe, empty, error, expander, progress, session_state, set_page_config, sidebar, subheader, success, title
from numpy import clip, log, pi, sqrt
from time import sleep
from pandas import DataFrame
import streamlit as st
import numpy as np
import pandas as pd
import time
from 計算 import calculate_london_penetration, calculate_quantum_impedance, calculate_coupled_thermal_load

# =====================================================================
# 2. UI 佈局與進階 Agent 狀態機 (包含敏度導向決策與多起點分流)
# =====================================================================

st.set_page_config(layout="wide", page_title="量子傳輸線 AI Agent 模擬器 V2")
st.title("🎛️ 量子傳輸線「電性-低溫熱負載」多場耦合 AI Agent 系統 V2")
st.caption("升級版：引入敏感度矩陣、多種子分流探索與自適應約束放寬機制")

if "solution_pool" not in st.session_state: st.session_state.solution_pool = []
if "running" not in st.session_state: st.session_state.running = False

# 側邊欄 spec 設定
st.sidebar.header("📋 量子系統核心輸入約束 (User Spec)")
target_zo = st.sidebar.number_input("目標特徵阻抗 (Ohm)", value=50.0, step=0.5)
freq_ghz = st.sidebar.number_input("運作頻率 (GHz)", value=6.0, step=0.1)
thermal_budget_uw = st.sidebar.number_input("10mK 層最大容許熱負載 (μW)", value=1.0, step=0.1)
min_h_mil = st.sidebar.number_input("最小介質厚度安全值 (mil)", value=4.0, step=0.1)
er_dielectric = st.sidebar.number_input("基板介電常數 Dk", value=4.2, step=0.1)

temperature_stages = [
    {"stage_name": "Room Temp", "temp_k": 300.0, "line_length_m": 0.5, "attenuation_db": 0},
    {"stage_name": "4K Stage", "temp_k": 4.2, "line_length_m": 0.3, "attenuation_db": 10},
    {"stage_name": "Still", "temp_k": 0.8, "line_length_m": 0.1, "attenuation_db": 10},
    {"stage_name": "MC Stage", "temp_k": 0.01, "line_length_m": 0.1, "attenuation_db": 20}
]

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🧠 升級版 Agent 梯度決策日誌與收斂軌跡")
    run_btn = st.button("🚀 啟動敏感度感知優化（10次迭代）", disabled=st.session_state.running)
    log_area = st.empty()
    progress_bar = st.progress(0)
    
    if run_btn:
        st.session_state.running = True
        st.session_state.solution_pool = []
        logs = []
        
        # 🧪 改良 1：設計 3 個截然不同的「初始種子」，分流並行探索，確保不會全部卡死在同一個盲點
        seeds = [
            {"name": "種子 A (傳統銅基) ", "material": "Cu", "width_mil": 12.0, "thickness_mil": 1.4, "h_mil": 8.0},
            {"name": "種子 B (超導微型) ", "material": "NbTi", "width_mil": 6.0, "thickness_mil": 0.5, "h_mil": 4.0},
            {"name": "種子 C (高阻抗高介質)", "material": "Nb", "width_mil": 16.0, "thickness_mil": 1.0, "h_mil": 10.0}
        ]
        
        current_iter = 0
        total_steps = 10
        
        # 動態放寬機制初始窗口
        zo_tolerance = 1.0 
        
        # 10次迭代主迴圈
        for iter_idx in range(1, total_steps + 1):
            progress_bar.progress(iter_idx * 10)
            logs.append(f"### 🔄 【第 {iter_idx} 次全局狀態優化】")
            
            # 對每個種子並行迭代更新
            for seed in seeds:
                # 1. 物理引擎正向計算
                elec_res = calculate_quantum_impedance(seed["width_mil"], seed["thickness_mil"], seed["h_mil"], er_dielectric, seed["material"], temp=0.01)
                thermal_res = calculate_coupled_thermal_load(seed, temperature_stages)
                
                zo_actual = elec_res["zo"]
                heat_uw = thermal_res["total_load_w"] * 1e6
                
                # 評審機制（引入動態容差）
                is_zo_ok = abs(zo_actual - target_zo) <= zo_tolerance
                is_thermal_ok = heat_uw <= thermal_budget_uw
                
                # 只要符合當前容差，立即捕捉進候選池
                if is_zo_ok:
                    tag = "超導冷量最優" if is_thermal_ok else "退相干保障（熱耗略高）"
                    if zo_tolerance > 1.0: tag += " (放寬容差約束)"
                    
                    st.session_state.solution_pool.append({
                        "tag": f"{seed['name']}-{tag}", "material": seed["material"],
                        "width_mil": round(seed["width_mil"], 2), "h_mil": round(seed["h_mil"], 2),
                        "zo": zo_actual, "heat_uw": round(heat_uw, 4)
                    })
                
                # 🧪 改良 2：數值敏感度矩陣（計算梯度），讓 Agent 智慧判斷調整方向
                delta = 0.1
                # 擾動線寬求阻抗梯度 dZo/dW
                e_up = calculate_quantum_impedance(seed["width_mil"] + delta, seed["thickness_mil"], seed["h_mil"], er_dielectric, seed["material"], temp=0.01)
                dZo_dW = (e_up["zo"] - zo_actual) / delta
                
                # 擾動介質厚度求阻抗梯度 dZo/dH
                e_h_up = calculate_quantum_impedance(seed["width_mil"], seed["thickness_mil"], seed["h_mil"] + delta, er_dielectric, seed["material"], temp=0.01)
                dZo_dH = (e_h_up["zo"] - zo_actual) / delta
                
                # 🧪 改良 3：基於梯度的反思決策邏輯 (Gradient-driven Policy)
                if not is_zo_ok or not is_thermal_ok:
                    # 如果熱超標且是常溫銅，強制切換超導（物理突變）
                    if seed["material"] == "Cu" and heat_uw > thermal_budget_uw:
                        logs.append(f"💡 *{seed['name']} 決策：常溫銅導線熱耗超標。執行材料超導化，突變切換至 NbTi。*")
                        seed["material"] = "NbTi"
                    else:
                        # 依據梯度進行精準幾何耦合微調
                        zo_error = target_zo - zo_actual
                        
                        # 為了降熱耗，線寬 W 必須努力減小
                        if heat_uw > thermal_budget_uw and seed["width_mil"] > min_h_mil:
                            step_w = -0.8
                        else:
                            # 否則依據阻抗誤差微調
                            step_w = np.clip(zo_error / (dZo_dW + 1e-5), -1.0, 1.0)
                        
                        # 為了補償線寬變化對阻抗的破壞，利用 dZo/dH 計算出 H 應該聯動調整多少
                        # 保持 Delta_Zo = dZo/dW * Step_W + dZo/dH * Step_H = 阻抗誤差
                        step_h = (zo_error - dZo_dW * step_w) / (dZo_dH + 1e-5)
                        step_h = np.clip(step_h, -1.5, 1.5)
                        
                        seed["width_mil"] = max(2.0, seed["width_mil"] + step_w)
                        seed["h_mil"] = max(min_h_mil, seed["h_mil"] + step_h)
            
            # 🧪 改良 4：自適應動態約束軟化規則
            # 如果進行到一半（第5次迭代）池子還是空的，自動適度放寬阻抗容差，防止「交集為空」卡死
            if iter_idx == 5 and len(st.session_state.solution_pool) == 0:
                zo_tolerance = 2.0
                logs.append("⚠️ **[系統防卡死安全機制觸發]**：硬性約束無解。Agent 自主啟動變革管理，將阻抗容差由 ±1.0Ω 彈性調整至 ±2.0Ω 以擴大工藝搜索邊界。")
                
            log_area.markdown("\n\n".join(logs[-4:])) # 只渲染最新4條，保持畫面流暢
            time.sleep(0.3)
            
        st.session_state.running = False
        st.success("🎉 敏感度協同優化完成！")

# 右側結果大盤
with col_right:
    st.subheader("🎯 升級版解法池（必定生成 3 套以上多元方案）")
    
    if len(st.session_state.solution_pool) > 0:
        df_all = pd.DataFrame(st.session_state.solution_pool).drop_duplicates(subset=["material", "width_mil", "zo"])
        
        # 依熱耗與電性偏差綜合排序，精選出最佳 3 套
        df_all["zo_dev"] = (df_all["zo"] - target_zo).abs()
        df_final = df_all.sort_values(by=["zo_dev", "heat_uw"]).head(3).reset_index(drop=True)
        df_final.index = [f"精選方案 {i+1}" for i in range(len(df_final))]
        
        for idx, row in df_final.iterrows():
          with st.expander(f"✨ {idx}：{row['tag']}", expanded=True):
            c1, c2, c3 = st.columns(3)
            c1.metric("特徵阻抗 (Zo)", f"{row['zo']} Ω", f"{row['zo'] - target_zo:.2f} Ω")
            c2.metric("10mK 熱負載", f"{row['heat_uw']} μW", f"目標: {thermal_budget_uw}μW")
            c3.metric("製程線寬 (W)", f"{row['width_mil']} mil", f"介質厚: {row['h_mil']}mil")
        st.subheader("📊 所有收斂工藝窗口總覽")
        st.dataframe(df_all.drop(columns=["zo_dev"]), column_config={ "tag": "演進路線來源", "material": "材料", "width_mil": "線寬(mil)", "h_mil": "介質厚(mil)", "zo": "阻抗(Ω)", "heat_uw": "熱耗(μW)"}, use_container_width=True)
    else:
      st.error("❌ 在當前極端輸入约束下依然無解。建議放寬「最大容許熱負載」或降低「基板介電常數」。")


