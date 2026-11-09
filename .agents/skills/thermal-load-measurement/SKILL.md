---
name: thermal-load-measurement
description: Use when the user needs to measure cryogenic thermal load across temperature stages for a transmission line or assembly, plan instrumentation/calibration/recording, or asks to 熱負載量測、低溫量測、cryogenic measurement、溫區熱負載.
---

# Thermal Load Measurement Capability（可移植）

本 skill 提供**低溫熱負載量測**的規劃與記錄結構。規範用中性佔位（6B）；公開單位（K、W、μW 等）與通用低溫量測/SOP 結構可保留。

## 量測目標（範本）
- 各 `<temperature_stage>` 的熱傳導/耗散貢獻（依模型拆分）。
- 關鍵 KPI（如 `<kpi_id>`）：指定溫區負載、總負載、每通道負載（單位明示）。
- 條件：安裝狀態、輸入功率/訊號、屏蔽與接地、熱平衡準則。

## 儀器與校準（通用類別）
- 溫度感測/校準：可追溯校準記錄。
- 熱功率施加與量測：來源、精度、配線/熱沉假設。
- 冷卻系統：達到並維持目標溫區的能力與穩定性。

## 量測流程（通用）
1. 確認溫區穩定與前置條件（真空/系統狀態/校準）。
2. 施加已知擾動/功率，等待熱平衡（判據明示），記錄觀測。
3. 依方法計算/推估熱負載；標註不確定性與假設。
4. 必要時量測元件耗散（如有輸入功率）。
5. 記錄可追溯資料（raw + derived + 條件）。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。溫度/狀態不穩、校準或追溯缺失、結果不明 → 停止，不得宣稱通過。

## 交棒（capability）
- 模擬/預估比對 → `design simulation capability`；SOP 細化 → `test/SOP capability`；材料屬性 → `material/component data capability`；裁決 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。公開低溫實務可提及溫區分層、熱平衡等待、重複量測；具體儀器型號、內部門檻與 `<workspace>` 記錄路徑依 6B/專案。