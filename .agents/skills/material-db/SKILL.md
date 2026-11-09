---
name: material-db
description: Use when the user needs to look up material properties, compare or accept material data/batches against criteria, or asks to 材質數據庫、material database、材料驗收、material properties、材料屬性查詢，as part of a design/test/acceptance workflow.
---

# Material/Component Data Capability（可移植）

本 skill 提供**材料/元件屬性查詢與驗收**能力。規範使用中性佔位（6B）；公開可引用標準（單位、通用屬性定義）可保留。

## 決策點
1. **查詢 vs 驗收**：查詢回傳屬性/來源/單位；驗收需比對 `<acceptance_criteria>` 並產出 pass/fail 證據。
2. **追溯性**：材料/批次/量測來源需可引用（record ref）；缺追溯不得宣稱驗收通過。
3. **交棒（capability）**：設計/模擬使用屬性時交由 `design simulation capability`；閘門裁決交由 `acceptance/KPI gate capability`；量測/SOP 交由 `test/SOP capability`。

## 屬性欄位慣例（可依領域擴充，公開單位可保留）
- 識別：`<material_id>`、類別（導體/超導體/介電質/其他）、來源/版本。
- 物性（示例類型）：臨界溫度、電阻率/導電性、熱傳導相關參數、密度、介電常數/損耗等；**單位必須明示**。
- 驗收：量測值 vs 期望/容差 → pass/fail + evidence ref。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）之 Delivery/KPI Gate 與 Evidence 欄位：
- 未達驗收準則或缺證據 → 不得宣稱材料/批次合格。
- 證據至少含 subject（材料/批次）、criteria/threshold、observed、pass/fail、timestamp/context、record ref。
- 狀態不明/追溯缺失 → stop-the-line。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。
- 可能的資料來源/工具：專案內材料資料庫模組或表格（`<workspace>/<material_db>`）；驗收函式/流程依專案實作。具體材料牌號、配方、廠商、內部門檻依 6B 處理。