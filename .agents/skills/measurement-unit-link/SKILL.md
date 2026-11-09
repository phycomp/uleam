---
name: measurement-unit-link
description: Use when the user needs to plan third-party or certified measurement collaboration, cross-check test results, or link acceptance evidence to external measurement capability, and asks to 量測單位、第三方驗證、交叉比對、外部量測、校準/驗證合作.
---

# External Measurement/Verification Capability（可移植）

本 skill 支援**外部量測/第三方驗證**的規劃與證據鏈結。規範用中性佔位（6B）；通用 SOP/驗證結構可保留。

## 流程（通用）
1. **盤點**：符合 `<measurement_scope>`（頻段/溫區/指標/可追溯性）能力的候選單位（>= `<n>` 依需求）。
2. **聯繫與範圍**：確認方法、校準追溯、報價/時程、樣品與資料要求。
3. **試量測/正式量測**：取得可追溯報告與原始/摘要數據。
4. **交叉比對**：內部 vs 外部結果建立比對表，差異分析與處置。
5. **結案證據**：將第三方報告納入 `<kpi_id>`/交付證據包。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。外部報告缺追溯/範圍不符/差異未處置 → 不得宣稱驗證完成。

## 交棒（capability）
- 測試方法 → `test/SOP capability`；KPI 裁決 → `acceptance/KPI gate capability`；索引 → `index/orchestration capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。具體機構名稱、合約、報價與內部 KPI 編號依專案/6B。