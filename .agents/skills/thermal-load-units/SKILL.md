---
name: thermal-load-units
description: Use when the user needs unit definitions/conversions or common pitfalls for thermal/electrical/mechanical quantities in cryogenic or transmission-line work, or asks to 熱負載單位、單位轉換、μW/W/mK/dB、unit conversion.
---

# Thermal/Engineering Units Capability（可移植）

本 skill 提供**單位與換算慣例**，降低數量級錯誤。公開 SI 單位與通用換算關係可保留（6B）。

## 常用單位（公開）
- 功率/熱負載：W, mW, μW（10^0 / 10^-3 / 10^-6 W）
- 熱導/熱導率：W/K, W/(m·K)（依語境）
- 溫度：K, mK
- 衰減/增益：dB（相對）；線性功率比需明確轉換
- 長度/幾何：m, mm, μm（及專案慣用單位時須標註換算）

## 換算與記錄要求
- 計算用基準單位、報告用可讀單位時，**必須顯式換算並標註單位**。
- 記錄欄位應含 `value + unit + condition/stage`（對齊 C1 Evidence）。
- dB 與線性量不可混用；溫度使用絕對溫標時需明示（如 K）。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：證據中的單位/條件缺失屬追溯缺陷；狀態不明 stop-the-line。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。專案可補充內部慣用單位（如 mil）與換算表；換算係數若採用需可追溯來源。