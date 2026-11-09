---
name: crosstalk-calc
description: Use when the user wants to calculate or evaluate crosstalk (e.g., NEXT/FEXT/total coupling loss) for a transmission-line or cryogenic cable design, assess coupling vs spacing/length/frequency assumptions, or asks to 串擾、crosstalk、NEXT、FEXT、耦合分析.
---

# Crosstalk Analysis Capability（可移植）

本 skill 提供**串擾/耦合估算**能力，依可追溯的幾何、頻率與模型假設輸出指標。規範用中性佔位（6B）；公開單位/通用模型結構可保留。

## 決策點
1. **輸入可追溯**：`<spec>`/幾何、耦合長度、間距、頻率/條件、模型假設必須明示；假設缺失 → 標註並不可作為驗收證據。
2. **估算 vs 驗收**：計算/模擬結果交由 `acceptance/KPI gate capability` 依 `<kpi_id>` 門檻裁決；量測比對交由 `test/SOP capability`。
3. **狀態不明**：模型不適用或輸入不可追溯 → stop-the-line（C1）。

## 輸出（建議）
- 指標：`<next>`, `<fext>`, `<total_crosstalk>`（單位明示，如 dB）與條件。
- 證據欄位：method/model ref、inputs/assumptions、observed/estimated、expected/threshold、pass/fail（若有門檻）、record ref。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。未達門檻/缺證據不得宣稱通過。

## 交棒（capability）
- 設計參數調整 → `design simulation capability` / `integration capability`。
- 量測 → `test/SOP capability`；材料/幾何資料 → `material/component data capability`；裁決 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。公開模型形式可描述，專案門檻/參數依 6B。
- 可能模型形式：NEXT/FEXT 估算與總串擾合成；實作可為 `<workspace>` 內計算模組（如 `evaluate_crosstalk(<spec>)` 類介面）。具体係數與門檻依專案驗證。