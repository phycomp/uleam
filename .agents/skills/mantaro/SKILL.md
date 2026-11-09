---
name: mantaro
description: Use when the user wants a calculator-style UI/workflow for impedance or transmission-line parameters (parameter inputs, unit toggles, result presentation), or asks to 阻抗計算器、stripline/microstrip UI、參數計算介面.
---

# Calculator UI/Workflow Capability（可移植）

本 skill 提供**參數計算器**的 UI/流程結構（輸入、單位切換、結果展示）。規範用中性佔位（6B）；公開工程概念可保留。

## 要點
- 輸入參數與單位明示（對齊 units capability）；預設值與假設可追溯。
- 計算模型/公式來源標註；結果為設計輔助，非驗收證據。
- 關鍵結果交 `design simulation capability`/`test/SOP capability` 驗證，裁決交 `acceptance/KPI gate capability`（C1）。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：未驗證不得宣稱達標；證據/單位缺失 stop-the-line。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。可用 Web/UI 框架實作輸入面板與結果卡；具體樣式、公式與專案參數依 6B/`<workspace>`。