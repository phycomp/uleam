---
name: thermal-load-sop
description: Use when the user needs a thermal-load measurement SOP/checklist (pre-checks, steps, anomaly handling, record format), or asks to 熱負載 SOP、量測標準作業、thermal measurement guidelines.
---

# Thermal Load SOP Capability（可移植）

本 skill 提供**熱負載量測 SOP 結構**。規範用中性佔位（6B）；公開單位與通用 SOP 結構可保留。

## SOP 結構（通用）
### 前置檢查
- 系統/溫區穩定、校準有效、追溯資訊（`<id>`, `<spec>`, 日期/操作者/條件）齊備。

### 量測步驟
- 設定條件 → 等待熱平衡（判據）→ 記錄 → 必要時重複/取統計 → 標註假設與不確定性。

### 異常處理
- 不穩定、數據異常、超出預期/預算：記錄現象，檢查錨定/屏蔽/接地/配線等；**狀態不明不得宣稱通過**。

### 記錄格式（建議，對齊 C1 Evidence）
`timestamp, subject/id, spec, stage/temp, condition, value, unit, method, pass_fail_or_pending, operator, evidence_ref, notes`

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。

## 交棒（capability）
- 量測執行細節 → `test/SOP capability`；模擬預期 → `design simulation capability`；裁決 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。具體等待時間、重複次數、內部門檻與表單路徑依 6B/專案。