---
name: nbtii-test-sop
description: Use when the user needs production test SOP for superconducting/cryogenic transmission-line builds (electrical, cryogenic, mechanical/environmental checks, records, CoC/evidence), and asks to 生產測試、test SOP、品質保證、QA、低溫測試流程.
---

# Production Test SOP Capability（可移植）

本 skill 提供**生產測試 SOP**結構，涵蓋電性、環境/低溫（如適用）、機械與出貨證據。規範用中性佔位（6B）；公開單位與通用 SOP 結構可保留。

## 測試項目（範本）
| 類別 | 項目 | 門檻/準則 | 條件/抽樣 |
|---|---|---|---|
| 電性 | 阻抗/絕緣/導通等 | `<limit>` | 全檢/抽樣 |
| 低溫/環境（如適用） | 臨界/轉變、溫區性能、循環 | `<limit>` | `<temperature_stage>`, `<cycles>` |
| 機械/可靠性（如適用） | 彎曲/拉力/熱衝擊等 | `<limit>` | 方法/標準 ref |

## SOP 與記錄
1. 依計畫執行全檢/抽樣；保留原始數據與追溯。
2. 記錄欄位對齊 C1 Evidence（id/batch/item/condition/value/unit/pass_fail/operator/timestamp/ref）。
3. 不合格隔離、失效分析、處置與重驗；出貨證據/CoC 僅在符合門檻且證據齊全時發出。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。狀態不明/缺證據不得宣稱合格或出貨可接受。

## 交棒（capability）
- 規格/門檻 → `acceptance/KPI gate capability`；量測方法 → `test/SOP capability`；材料 → `material/component data capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。具體 Tc/Ic/阻抗門檻、抽樣等級、MES/CoC 格式與材料體系依 6B/專案。