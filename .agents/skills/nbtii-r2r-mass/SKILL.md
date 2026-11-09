---
name: nbtii-r2r-mass
description: Use when the user needs roll-to-roll or high-volume continuous manufacturing workflow guidance, in-line control/traceability, and quality gates, and asks to R2R、捲對捲、大量生產、high-volume manufacturing、連續製程.
---

# Continuous / High-Volume Manufacturing Capability（可移植）

本 skill 提供**連續/大量製程**（如 R2R 類）的控制與追溯結構。規範用中性佔位（6B）；通用製程控制/SOP 結構可保留。

## 控制重點
- 連續製程參數（張力/速度/對位/厚度/清潔度等）與 in-line 監測。
- 缺陷偵測與分級處置；批次/捲/件追溯。
- 變更控制與重驗；抽樣/全檢策略對齊風險與 `<kpi_id>`。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line、Change control。

## 交棒（capability）
- 測試/SOP → `test/SOP capability`；材料 → `material/component data capability`；裁決 → `acceptance/KPI gate capability`；整合 → `integration capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。具體設備、AOI 規則、材料體系與門檻依 6B/專案。