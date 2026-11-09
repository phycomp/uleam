---
name: kpi-delivery-valid
description: Use when the user wants a KPI/delivery validation pipeline from spec to acceptance, needs per-stage KPI verification or evidence structure, or asks to KPI 交付、KPI 驗收、驗證 pipeline、spec→delivery、各階段 gate、未達標能否交付.
---

# KPI Delivery & Validation Capability（可移植）

本 skill 定義**KPI 規格到交付驗收**的 capability 流程與閘門要求。規範用中性佔位（6B）；公開標準可保留。**未達門檻/缺證據不得宣稱完成。**

## Capability Flow（非 skill ID）
`spec/KPI definition` → `development/design` → `test/measurement` → `verification` → `delivery` → `usage+test+data records` → `acceptance/KPI gate`

## 階段要求（最小集）
1. **Spec/KPI definition**：定義 `<kpi_id>`、目標、門檻、方法、負責與時程語意；版本化。
2. **Development/design**：實作/設計產物可追溯到 KPI/spec。
3. **Test/measurement**：執行測試或量測，保留命令/程序與原始結果。
4. **Verification**：比對 observed vs expected/threshold，產出 pass/fail 與證據 ref。
5. **Delivery**：交付包含程式/文件/測試/驗證證據；不得以「可編譯/看起來完成」替代驗證。
6. **Usage + test + data records**：使用說明、測試指引、資料/材料記錄可追溯。
7. **Acceptance/KPI gate**：彙總各 `<kpi_id>` 結果；任一必要 gate 未過 → 不得宣稱整體交付完成，回到負責 capability。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：
- Gate rule / Evidence 最小欄位 / Stop-the-line / Change control 全部適用。
- 證據至少含：`<artifact_id|kpi_id>`, subject, stage, method/procedure ref, expected threshold, observed result, pass/fail, timestamp, owner/context, evidence path/record ref。

## 交棒（capability）
- 設計/計算問題 → `design simulation capability`。
- 材料/元件資料問題 → `material/component data capability`。
- 測試/SOP 執行問題 → `test/SOP capability`。
- 整合問題 → `integration capability`。
- 能力選路 → `index/orchestration capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。
- `<workspace>` 可能有 KPI 追蹤/驗證模組、測試指南、合規文件與領域 skills；具體檔名、門檻值、內部流程依 6B。
