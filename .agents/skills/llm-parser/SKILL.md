---
name: llm-parser
description: Use when the user wants to parse natural-language descriptions into structured transmission-line or engineering parameters (with heuristic fallback when model/API is unavailable), or asks to LLM 解析、自然語法、參數生成、語意解析.
---

# NL/LLM Parameter Parsing Capability（可移植）

本 skill 將自然語言描述轉為**結構化參數**（如通道、幾何、材料類別、頻率/條件）。規範用中性佔位（6B）；輸出需可追溯與可驗證。

## 決策點
1. **可用性**：LLM/API 不可用時使用啟發式/規則 fallback，並標註來源與信心/限制。
2. **驗證**：解析結果是設計輸入，非驗收證據；關鍵參數需由 `design simulation capability` / `test/SOP capability` / `acceptance/KPI gate capability` 依 C1 驗證。
3. **不確定性**：模糊/缺失欄位輸出為 `<unknown>` 或假設清單，不得靜默猜測為已確認。

## 輸出（建議）
- `parameters`（結構化）、`assumptions`、`source`（llm|heuristic|mixed）、`warnings`。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：關鍵結論/交付仍需 Evidence 與 gate；狀態不明 stop-the-line。

## 交棒（capability）
- 設計/計算 → `design simulation capability`；裁決 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。`<workspace>` 可能包含解析模組與目標準確率/KPI；具體模型、門檻與路徑依 6B。