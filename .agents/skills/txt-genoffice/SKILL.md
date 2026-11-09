---
name: txt-genoffice
description: Use when the user wants to convert text/markdown into presentation slides (PPTX or equivalent) using a document-generation pipeline, with theme/compact/layout options and verification, or asks to 文字轉投影片、text to slides、markdown to pptx、簡報產生、presentation pipeline.
---

# Text-to-Presentation Pipeline Capability（可移植）

本 skill 提供**文字/Markdown → 投影片**的轉換流程結構。規範用中性佔位（6B）；公開格式/工具類型可保留，具體路徑與實作置於 1b。

## 決策點
1. **輸入/輸出**：`<input>`（text/markdown/spec）→ `<slides_model>` → `<output_artifact>`（如 PPTX）；保留來源可追溯。
2. **選項**：主題/樣式、合併/compact、字型大小/版面約束；選項需記錄於產出 metadata/證據。
3. **驗證**：產物可開啟/結構正確/關鍵內容存在；自動化檢查或測試通過才可宣稱完成（C1）。

## 流程（範本）
1. 解析輸入為投影片結構（標題、要點、分節）。
2. 套用主題/版面規則；處理溢位與 compact 合併（如啟用）。
3. 產生輸出檔與 metadata。
4. 執行驗證（檔案存在、格式檢查、測試、抽樣檢視）；記錄 evidence。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。轉換失敗、產物損壞或未驗證 → 不得宣稱完成。

## 交棒（capability）
- 內容/規格品質 → 上游內容能力；驗收 → `acceptance/KPI gate capability`；重構/整合 → `index/orchestration capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。`<workspace>` 可能使用 CLI/函式庫將 text→markdown/slides→PPTX；具體 repo 路徑、命令、主題名稱、測試腳本與輸出路徑依 6B/專案環境。