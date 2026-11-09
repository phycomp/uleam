---
name: electrical-test-sop
description: Use when the user needs an electrical test SOP (TDR/VNA/S-parameters/insulation/crosstalk, room/low-temperature conditions), test steps, or record formats, and asks to 電性測試、electrical test SOP、TDR、VNA、S參數測試.
---

# Electrical Test SOP Capability（可移植）

本 skill 提供**電性測試 SOP 結構**（計畫、步驟、記錄、異常處理）。規範用中性佔位（6B）；公開單位與通用 SOP 結構可保留。

## 測試項目（可裁剪）
| 類別 | 項目 | 指標/門檻 | 條件/儀器 |
|---|---|---|---|
| 常溫/基準 | 阻抗/TDR、S參數、反射、絕緣等 | `<limit>` | `<method>`、`<condition>` |
| 環境/低溫（如適用） | 指標於溫區/循環 | `<limit>` | `<temperature_stage>`、循環次數 |
| 串擾/耦合（如適用） | NEXT/FEXT 等 | `<limit>` | 鄰道/頻率 |

## SOP 流程（通用）
1. 前置：校驗儀器、確認樣品/`<spec>`/追溯資訊。
2. 執行：按項目量測，保留原始數據與條件。
3. 記錄：寫入可追溯記錄（見下）。
4. 判定：比對門檻 → pass/fail；不合格隔離並啟動失效分析/處置流程。
5. 報告：交付證據與結論；未驗證項明列。

## 記錄欄位（建議）
`<serial_or_id>, <batch_or_lot>, test_item, condition/freq, value, unit, stage/temp, pass_fail, operator, timestamp, evidence_ref`（依 C1 Evidence 對齊）。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。量測狀態不明/追溯缺失 → 停止，不得宣稱通過。

## 交棒（capability）
- 規格/門檻來源 → electrical specification / `acceptance/KPI gate capability`；材料資料 → `material/component data capability`；裁決 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。具體儀器型號、抽樣計畫（AQL 等）、內部門檻與 MES 欄位依專案/6B。