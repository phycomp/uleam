---
name: three-view
description: Use when the user needs front/side/top (or equivalent) technical views for a component/stack/spec, with configurable labels, units, and scale, or asks to 三視圖、前視圖、側視圖、上視圖、工程視圖.
---

# Technical Views Capability（可移植）

本 skill 提供**工程視圖**（前/側/上等）生成結構。規範用中性佔位（6B）；公開繪圖/標註慣例可保留。

## 要點
- 視圖由 `<spec>`/幾何驅動；單位、比例、標註明示。
- 視圖為溝通/檢視產物；作為驗收證據時需對應量測/檢驗記錄（C1）。
- 字型/縮放/匯出為表現設定，不改變規格真值。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：視圖聲稱若影響交付結論，需可追溯證據；不確定 stop-the-line。

## 交棒（capability）
- 設計來源 → `design simulation capability`；驗收 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。`<workspace>` 可能提供繪圖函式/模組；具體 API 與路徑依 6B。