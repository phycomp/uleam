## 3. LangGraph 決策節點與優化邏輯 (Nodes & Edges)
# 在這裡，我們將您的優化策略硬編碼進邏輯中：
# 優化順序：優先切換材料（例如銅線換成超導 NbTi 線，直接消除導線衰減自發熱），若仍不達標，再微調幾何截面（把線變細）。
# 最高指標：只要阻抗偏離 $50 \pm 1$ 歐姆，或相位雜訊超出退相干預算，該方案直接判定失敗，重回優化循環。

from langgraph.graph import StateGraph, END
workflow = StateGraph(AgentState)
def init_design_node(state: AgentState): # 節點 1：初始化設計
 # LLM 讀取 User Spec，選擇初始材料與疊構（需過濾：硬規則必須對稱）
 # 輸出符合對稱性、介質厚度安全值的初始 stackup
 return {"current_stackup": initial_symmetric_stackup, "iteration_count": 0}

def electrical_calc_node(state: AgentState): # 節點 2：電性模擬（含超導穿透與動態電感）
 stackup = state["current_stackup"]
 # 呼叫工具計算阻抗與損耗
 res = calculate_quantum_impedance(..., material=stackup[0]['material'])
 return {"electrical_results": res}

def thermal_calc_node(state: AgentState): # 節點 3：熱負載動態耦合模擬
 # 呼叫工具進行傅立葉積分與衰減器自發熱耦合計算
 res = calculate_coupled_thermal_load(state["current_stackup"], state["temperature_profile"])
 return {"thermal_results": res}

def quantum_coherence_review_node(state: AgentState): # 節點 4：量子退相干風險評審與優化決策（核心 AI 決策點）
 zo = state["electrical_results"]["zo"]
 total_heat = state["thermal_results"]["total_load_w"]
 iter_idx = state["iteration_count"]

 # 決策邊界檢查：
 # 1. 電性硬指標：阻抗必須完美匹配 50 歐姆，否則反射導致訊號衰減與量子比特退相干
 # 2. 熱指標：低溫冷量預算
 is_zo_ok = (49.0 <= zo <= 51.0)
 is_thermal_ok = (total_heat < 10e-6) # 假設混冷層極限 10微瓦

 if is_zo_ok and is_thermal_ok:
   # 雙指標達標，將此方案收入 Solution Pool
   state["solution_pool"].append({
     "stackup": state["current_stackup"],
     "elec": state["electrical_results"],
     "thermal": state["thermal_results"]
   })

 # 檢查是否收集滿 3 套方案，或達到最大迭代次數 (e.g., 10次)
 if len(state["solution_pool"]) >= 3 or iter_idx >= 10:
   return {"iteration_count": iter_idx + 1} # 準備走向結束

 # 💡 團隊核心策略硬編碼：優化路徑決策
 next_stackup = state["current_stackup"].copy()
 if not is_thermal_ok and is_zo_ok:
   # 電性好但熱負載超標 -> 依據您的決策：優先調材料，再調幾何
   if next_stackup[0]['material'] == "Cu":
     # 優先級 1：調整材料（銅換超導 NbTi，大幅降低熱導與損耗）
     next_stackup[0]['material'] = "NbTi"
   else:
     # 優先級 2：材料已是超導，調整幾何（把線變細以阻絕固體熱傳導）
     next_stackup[0]['width_mil'] -= 0.5
     # 為了維持 50 歐姆，線變細時，介質厚度 h 或介電常數必須聯動調整
     next_stackup[1]['thickness_mil'] -= 0.3

 return {"current_stackup": next_stackup, "iteration_count": iter_idx + 1}

def solution_generator_node(state: AgentState): # 節點 5：方案生成器（滿足選項 C）
 # 從 solution_pool 中挑選出最優（或最具代表性）的三套方案
 # 方案 1：電性極致表現型（阻抗完美 50.00 Ohm）
 # 方案 2：低溫熱負載極小化型（最省冷量）
 # 方案 3：製程良率平衡型（線寬介質厚度取中間值）
 final_three = select_top_three(state["solution_pool"])
 return {"final_solutions": final_three}

def should_continue(state: AgentState): # 定義工作流條件分支 Edge
 if len(state["solution_pool"]) >= 3 or state["iteration_count"] >= 10:
   return "generate_final"
 return "loop_optimize"

