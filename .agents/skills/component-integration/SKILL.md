---
name: component-integration
description: Use when the user wants to integrate components (e.g., attenuator, filter, thermal/radiation control elements) into a transmission-line or system stack, define component parameters, or validate integration impacts, or asks to 元件整合、衰減器、濾波器、整合設計、component integration.
---

# Integration Capability（可移植）

本 skill 處理**元件/子系統整合設計**：選型參數、堆疊/介面整合、對關鍵指標（電性/熱/機構/訊號等）的影響評估。規範用中性佔位（6B）；公開物理/工程公式與單位可保留。

## 決策點
1. **整合目標與約束**：明確 `<spec>`（介面、頻段/訊號、熱預算、空間、可靠性等）。
2. **參數與模型**：元件參數必須可追溯（datasheet/量測/假設）；假設需標註。
3. **驗證交棒**：整合後影響由 `design simulation capability` 或 `test/SOP capability` 評估；是否可交付由 `acceptance/KPI gate capability` 裁決。

## 常見元件類型（可擴充，公開概念）
- 能量/訊號調整元件（如衰減/增益相關）：關注插損、功耗/自發熱、匹配。
- 頻率選擇/濾波元件：關注截止/帶寬、阻帶、對系統雜訊的影響。
- 熱/輻射管理元件：關注熱負載、輻射遮蔽、溫區約束。
- 介面/連接元件：交由介面/連接能力與 SOP 驗證。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：
- 整合結論需有可追溯假設與證據；未驗證影響不得宣稱達標。
- 關鍵 KPI/門檻由 acceptance/KPI gate 裁決；狀態不明 stop-the-line。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。
- `<workspace>` 專案可能包含元件整合模組/腳本與 stack 設計流程；具體元件型號、內部門檻與佈局依 6B 處理。
