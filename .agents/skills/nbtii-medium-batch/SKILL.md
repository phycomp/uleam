---
name: nbtii-medium-batch
description: Use when the user needs pilot/medium-batch production planning and control (process window, yield baseline, traceability, sampling tests), and asks to 中量生產、試產、pilot run、batch manufacturing、良率追溯.
---

# Pilot / Medium-Batch Production Capability（可移植）

本 skill 提供**試產/中批量**製程控制與證據結構。規範用中性佔位（6B）；通用 SPC/追溯/SOP 結構可保留。

## 適用
- 試產/中批量（`<batch_size>` 範圍由專案定義），目標建立製程窗口、良率基線與追溯。

## 控制重點
- 製程參數窗口與 SOP；關鍵尺寸/性能管控。
- 追溯：材料/批次/設備/人員/時間/參數。
- 首件/變更點驗證；異常與失效分析閉環。
- 測試策略：全檢/抽樣由風險與 `<kpi_id>` 決定，記錄可追溯。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line、Change control。製程或 KPI 變更需版本化並重驗。

## 交棒（capability）
- 測試/SOP → `test/SOP capability`；材料 → `material/component data capability`；裁決 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。具體 Cp/Cpk 門檻、抽樣計畫、MES 欄位與材料體系依 6B/專案。