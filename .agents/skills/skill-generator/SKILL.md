---
name: skill-generator
description: Use when the user wants to generate a skill/module scaffold from a spec plus repository context (AST/structure) and policy, including core code and tests, or asks to 產生 skill、生成代理人、spec to code、scaffold skill with tests.
---

# Skill/Module Generator Capability（可移植）

本 skill 提供**由規格 + repo 上下文 + 政策生成 skill/模組與測試**的流程。規範用中性佔位（6B）；應保留證據與人工審查閘門。

## 流程（範本）
1. **盤點上下文**：掃描 `<repo_path>` 結構/AST/介面；記錄範圍與限制。
2. **規格/政策審查**：識別模糊、衝突與禁止推論區；不確定/違反政策 → 停止並回報（stop-the-line）。
3. **設計**：衝突處置、相容/adapter 策略、需人工確認的推論點（明確標註 TODO/assumption）。
4. **生成**：核心程式 + 測試；避免靜默猜測關鍵行為。
5. **驗證**：語法/靜態檢查、測試執行、證據記錄；未通過不得宣稱可用。
6. **落盤**：輸出到 `<output_dir>`，保留生成來源與版本資訊。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line、Change control。生成物需測試/驗證證據；模糊高風險推論不可冒充確認事實。

## 交棒（capability）
- 領域驗收 → `acceptance/KPI gate capability`；整合/重構 → `index/orchestration capability` / restructure capability；測試 → `test/SOP capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。具體 prompt 檔、工具鏈、輸出目錄與執行器依 6B/`<workspace>`。