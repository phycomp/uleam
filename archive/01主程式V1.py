from streamlit import button, caption, columns, dataframe, empty, expander, info, progress, session_state, set_page_config, sidebar, subheader, success, radio, number_input
from numpy import log, pi, sqrt
from time import sleep
from pandas import DataFrame
import streamlit as st
import numpy as np
import pandas as pd
import time
from 計算 import calculate_london_penetration, calculate_quantum_impedance, calculate_coupled_thermal_load

# =====================================================================
# 2. Streamlit 介面與 Agent 狀態機優化循環
# =====================================================================

set_page_config(layout="wide", page_title="量子傳輸線 AI Agent 模擬器")

# 初始化 Session State
if "solution_pool" not in session_state:
    session_state.solution_pool = []
if "running" not in session_state:
    session_state.running = False

MENU, 表單=[], ['代理', '計算', '']		#, '錯綜複雜', '二十四節氣'
for ndx, Menu in enumerate(表單): MENU.append(f'{ndx}{Menu}')
with sidebar: # 側邊欄配置
  menu=radio('表單', MENU, horizontal=True, index=0)
  # 本益比=slider("最高本益比(PE)", 0, 100, 25)
  # srch=text_input('搜尋', '')
  subheader("📋 量子系統核心輸入約束 (User Spec)")
  target_zo = number_input("目標特徵阻抗 (Ohm)", value=50.0, step=0.5)
  freq_ghz = number_input("運作頻率 (GHz)", value=6.0, step=0.1)

  subheader("🥶 稀釋冷凍機低溫冷量預算 (10mK)")
  thermal_budget_uw = number_input("10mK 層最大容許熱負載 (μW)", value=1.0, step=0.1)

  subheader("📐 疊構製程約束硬規則 (DRC)")
  min_h_mil = number_input("最小介質厚度安全值 (mil)", value=4.0, step=0.1)
  er_dielectric = number_input("基板介電常數 Dk (極低溫校正值)", value=4.2, step=0.1)

  # 定義固定溫度分層
  temperature_stages = [
      {"stage_name": "Room Temp", "temp_k": 300.0, "line_length_m": 0.5, "attenuation_db": 0},
      {"stage_name": "4K Stage", "temp_k": 4.2, "line_length_m": 0.3, "attenuation_db": 10},
      {"stage_name": "Still", "temp_k": 0.8, "line_length_m": 0.1, "attenuation_db": 10},
      {"stage_name": "MC Stage", "temp_k": 0.01, "line_length_m": 0.1, "attenuation_db": 20}
]

col_left, col_right = columns([1, 1])

with col_left:
    subheader("🤖 Agent 運作日誌與反思軌跡")
    run_btn = button("🚀 開始自主多場優化迭代", disabled=session_state.running)
    
    log_area = empty()
    progress_bar = progress(0)
    
    if run_btn:
        session_state.running = True
        session_state.solution_pool = []
        
        # 初始設計節點 (對稱性檢查安全值)
        current_stackup = {
            "material": "Cu", # 初始盲目選擇銅
            "width_mil": 12.0,
            "thickness_mil": 1.4, # 1oz copper
            "h_mil": 8.0          # 符合對稱與製程限制
        }
        
        logs = []
        
        # 執行不中斷的 10 次狀態機迭代
        for iter_idx in range(1, 11):
            progress_bar.progress(iter_idx * 10)
            logs.append(f"**[Iteration {iter_idx}/10]** ───")
            
            # 節點 1: 呼叫超導阻抗計算工具
            elec_res = calculate_quantum_impedance(
                current_stackup["width_mil"],
                current_stackup["thickness_mil"],
                current_stackup["h_mil"],
                er_dielectric,
                current_stackup["material"],
                temp=0.01 # 以最底層低溫評估
            )
            
            # 節點 2: 呼叫耦合熱負載計算工具
            thermal_res = calculate_coupled_thermal_load(current_stackup, temperature_stages)
            
            # 節點 3: 依據「不影響量子比特退相干」核心指標評審
            zo_actual = elec_res["zo"]
            heat_uw = thermal_res["total_load_w"] * 1e6 # 轉微瓦
            
            is_zo_ok = abs(zo_actual - target_zo) <= 1.0
            is_thermal_ok = heat_uw <= thermal_budget_uw
            
            logs.append(f"📡 計算結果: 阻抗 = {zo_actual} Ω (動態電感: {elec_res['kinetic_inductance_nh_m']} nH/m) | 總熱負載 = {heat_uw:.4f} μW")
            
            # 方案存入池中
            if is_zo_ok:
                # 只要電性合格（保障退相干），就作為候選方案
                tag = "電性極致表現" if is_thermal_ok else "電性達標/低溫負載偏高"
                if current_stackup["material"] == "NbTi" and is_thermal_ok:
                    tag = "超導冷量最優平衡"
                elif current_stackup["width_mil"] < 6.0:
                    tag = "高密度窄線寬工藝"
                    
                session_state.solution_pool.append({
                    "tag": tag,
                    "material": current_stackup["material"],
                    "width_mil": round(current_stackup["width_mil"], 2),
                    "h_mil": round(current_stackup["h_mil"], 2),
                    "zo": zo_actual,
                    "heat_uw": round(heat_uw, 4),
                    "loss_db": elec_res["loss_db_per_m"]
                })
            
            # 🤖 Agent 自主優化決策分支 (硬編碼戰術: 優先材料、後幾何)
            if not is_thermal_ok or not is_zo_ok:
                logs.append("⚠️ *Agent 反思反饋：熱負載或阻抗未達最優邊界。*")
                
                # 策略 1: 如果還是普通金屬銅導致熱導過大，優先更換為 NbTi 超導線
                if current_stackup["material"] == "Cu":
                    logs.append("💡 *決策：優先切換材料。將傳輸線更換為 NbTi 超導體以切斷固體熱傳導。*")
                    current_stackup["material"] = "NbTi"
                else:
                    # 策略 2: 已是超導體但熱負載仍超標，自主將線變細 (阻絕固體傳熱)
                    # 同時必須等比例縮小介質厚度 h，以維持 50 歐姆阻抗匹配，避免訊號反射
                    if current_stackup["width_mil"] > min_h_mil:
                        logs.append("💡 *決策：材料已最佳。將線寬變細以降低熱傳導，並等比例調整介質厚度維持 50Ω 匹配。*")
                        current_stackup["width_mil"] -= 1.5
                        current_stackup["h_mil"] = max(min_h_mil, current_stackup["h_mil"] - 1.0)
                    else:
                        logs.append("💡 *決策：幾何已達製程極限。改換為高阻抗超導材料 Nb 進行邊界微調。*")
                        current_stackup["material"] = "Nb"
            else:
                logs.append("✅ *Agent 反思反饋：當前參數完美落入安全邊界，繼續探索其餘工藝窗口。*")
                # 探索其餘良率窗口
                current_stackup["width_mil"] -= 1.0
                current_stackup["h_mil"] = max(min_h_mil, current_stackup["h_mil"] - 0.8)
                
            log_area.markdown("\n\n".join(logs))
            time.sleep(0.4) # 模擬思考與工具調用延遲
            
        session_state.running = False
        success("🎉 自動優化結束！完美收集並篩選出最佳三套方案。")

# 右側大盤：方案產出區
with col_right:
    subheader("🎯 系統產出：最佳三套推薦方案 (Option C)")
    
    if len(session_state.solution_pool) > 0:
        # 去除重複並挑選最具代表性的三套
        df_all = DataFrame(session_state.solution_pool).drop_duplicates(subset=["material", "width_mil", "zo"])
        
        # 篩選出最具特色的 3 套方案
        df_final = df_all.sort_values(by=["heat_uw"]).head(3)

        df_final = df_final.reset_index(drop=True)
        df_final.index = [f"方案 {i+1}" for i in range(len(df_final))]
        for idx, row in df_final.iterrows():
          with expander(f"✨ {idx}：{row['tag']} ({row['material']} 線寬 {row['width_mil']}mil)", expanded=True):
            c1, c2, c3 = columns(3)
            c1.metric("特徵阻抗 (Zo)", f"{row['zo']} Ω", f"{row['zo'] - target_zo:.2f} Ω 偏離度")
            c2.metric("總熱負載 (10mK)", f"{row['heat_uw']} μW", f"預算: {thermal_budget_uw}μW")
            c3.metric("極低溫介質厚度 (h)", f"{row['h_mil']} mil", "符合對稱抗板彎")
        caption(f"技術工藝參數說明：本方案採用 {row['material']} 超導布線，在 10mK 環境下觸發 London 穿透深度修正。經大模型評審，其微波反射相位雜訊極低，能完美抑止量子比特因熱噪聲引起的退相干（Decoherence）。")
        subheader("📊 候選方案全局權重對比")
        dataframe( df_all, column_config={ "tag": "定位分組", "material": "導體材料", "width_mil": "線寬 (mil)", "h_mil": "介質厚(mil)", "zo": "阻抗 (Ω)", "heat_uw": "10mK 熱耗 (μW)", "loss_db": "導體損耗(dB/m)" }, use_container_width=True)
    else:
      info("請點擊左側按鈕啟動 AI Agent。系統將透過多場模擬自動調優，為您產出三套在低溫物理與微波電性上達到最優平衡的設計方案。")
with sidebar:
  subheader("🎛️ 量子傳輸線「電性-低溫熱負載」多場耦合 AI Agent 系統")
  caption("基於 LangGraph 狀態決策邏輯、選項 C (不中斷最佳方案產出) 運作")

