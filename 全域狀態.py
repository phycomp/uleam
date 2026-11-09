## 1. 全域狀態定義 (State)
# 我們使用 Python 的 TypedDict 來定義 LangGraph 的狀態。狀態中必須包含溫度分層（常溫到 10mK 的陣列）以及傳輸線在各層的幾何與材料屬性。

from typing import TypedDict, List, Dict, Any

class LayerStackup(TypedDict):
    layer_id: int
    name: str             # e.g., "Top_Trace", "Dielectric_1"
    material: str         # e.g., "NbTi", "Cu", "FR4", "Sapphire"
    thickness_mil: float  # 介質厚度（硬規則：不可小於製程極限）
    width_mil: float      # 線寬
    spacing_mil: float    # 線距 (CPW 適用)

class TemperatureStage(TypedDict):
    stage_name: str       # e.g., "300K", "4K", "Still_800mK", "MC_10mK"
    temp_k: float         # 該層實體溫度
    line_length_m: float  # 傳輸線在該溫區的長度
    attenuation_db: float # 該溫區佈署的微波衰減器阻值 (用於計算 Attenuator Dissipation)

class AgentState(TypedDict):
    # 輸入約束
    target_zo: float                       # 目標阻抗，通常為 50.0 Ohm
    frequency_ghz: float                   # 運作頻率，如 4-8 GHz
    temperature_profile: List[TemperatureStage]
    
    # 目前設計狀態
    current_stackup: List[LayerStackup]    # 必須符合對稱性硬規則
    is_symmetric: bool                     # 防板彎檢查結果
    
    # 模擬計算結果
    electrical_results: Dict[str, Any]     # 阻抗 (含動態電感修正), RL, IL, Phase Noise
    thermal_results: Dict[str, Any]        # 固體熱傳導, 衰減器自發熱, 總熱負載 (W)
    
    # 評估與迭代
    coherence_score: float                 # 退相干風險評估分數
    iteration_count: int                   # 目前迭代次數
    solution_pool: List[Dict[str, Any]]    # 收集符合標準的候選方案（目標收集滿 3 套）
