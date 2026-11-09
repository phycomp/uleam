---
name: connector
description: Use when the user needs RF/cryogenic connector selection guidance, interface compatibility checks, or connector test/SOP structure (electrical, mechanical, environmental), and asks to 連接器、connector、SMA/SMP/精密同軸、VSWR、連接器測試.
---

# Connector Selection & Test Capability（可移植）

本 skill 提供**連接器選型與測試**的結構化能力。規範用中性佔位（6B）；公開單位與通用測試/SOP 結構可保留。

## 選型（範本）
| 面向 | 準則/欄位 | 佔位 |
|---|---|---|
| 頻率/頻寬 | 系統需求 + 餘裕 | `<freq_range>`, `<margin>` |
| 電性 | 反射/損耗/相位穩定 | `<vswr_rl>`, `<il>`, `<phase>` |
| 機械 | 插拔壽命、扭力、尺寸/介面 | `<durability>`, `<torque>` |
| 環境/溫區 | 材料相容、熱循環、可靠性 | `<temperature_stage>`, `<cycles>` |
| 系統整合 | 密度、可維護性、成本/供應 | `<constraints>` |

## 測試 SOP（通用）
- **電性**：S參數/反射/損耗/相位；條件與方法可追溯。
- **機械**：插拔/扭力/振動衝擊（依適用標準）；前後性能比對。
- **環境**：溫區/循環後性能；記錄不確定性與異常。
- **記錄**：`<id>`, type/interface, condition, metrics, unit, pass_fail, operator, timestamp, evidence_ref（對齊 C1）。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。選型假設/測試狀態不明不得宣稱符合。

## 交棒（capability）
- 規格門檻 → electrical specification / `acceptance/KPI gate capability`；整合 → `integration capability`；測試執行 → `test/SOP capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。公開可提及常見同軸介面家族與「頻率/VSWR/壽命/溫區相容」選型面向；具體型號、門檻、供應商與內部標準依 6B/專案。