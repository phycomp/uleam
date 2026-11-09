---
name: thermal-load-simulation
description: Use when the user wants to simulate or estimate cryogenic thermal load (conduction/dissipation components, temperature stages, material/geometry assumptions), or asks to 熱負載模擬、熱負載計算、thermal load simulation、預估熱負載.
---

# Thermal Load Simulation Capability（可移植）

本 skill 提供**熱負載估算/模擬**能力，用於設計預估與敏感性分析。規範用中性佔位（6B）；公開單位與通用熱傳/功率關係結構可保留。

## 決策點
1. **假設可追溯**：材料屬性、幾何、溫區邊界、耗散模型、接觸/錨定假設必須明示；來源交由 `material/component data capability` 或記錄。
2. **估算≠驗收**：模擬輸出供設計與驗證規劃；達標裁決由 `acceptance/KPI gate capability`，量測由 `test/SOP capability`。
3. **不確定性**：關鍵參數敏感時應標註範圍/情境；不可用單點結果宣稱保證通過。

## 模型構成（範本）
- 傳導/結構熱負載：依 `<material>`、`<geometry>`、`<temperature_stage>` 與選定模型積分/估算。
- 元件耗散（如適用）：依輸入功率與元件模型估算。
- 總負載與分項：`<total>`、`<by_component>`、`<by_stage>`，單位明示。

## 輸出/證據
- inputs/assumptions、model ref、computed/estimated results、comparison to `<targets|kpi_id>`（若有）、pass/fail 僅在有明確門檻且方法適用時標註，否則標註「待驗證」。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。模型/輸入不可追溯或狀態不明 → stop-the-line。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。公開可提及傅立葉熱傳導類模型與耗散分項概念；具體係數、材料表、腳本路徑與門檻依 6B/`<workspace>`。