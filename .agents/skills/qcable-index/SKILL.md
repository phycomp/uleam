---
name: qcable-index
description: Use when the user wants an index/map of quantum-cable or related engineering capabilities, needs to choose a capability/subdomain for a task, or asks to 技能索引、能力圖、量子傳輸線能力、which capability to use、熱負載/規格/串擾/電性/SOP/連接器 對應哪個能力.
---

# QCable Capability Index（index/orchestration capability）

本 skill 提供**受控 capability/子域地圖**，協助選路；不綁定 sibling skill ID。規範判定與證據要求引用 `qcable-contracts`（C1）。

## Capability / 子域地圖（受控列舉）

| 子域 | 能力 | 典型觸發/輸入 | 交付/證據 |
|---|---|---|---|
| 設計與模擬 | `design simulation capability` | 規格、阻抗/幾何/疊構、模擬假設 | 可追溯參數、模擬/計算結果、假設清單 |
| 熱負載 | `design simulation capability` / `test/SOP capability` | 溫區、材料、功耗、量測條件 | 熱負載計算或量測紀錄、單位明示、證據 ref |
| 元件/材料 | `material/component data capability`、`integration capability` | 材料屬性、元件參數、堆疊 | 屬性/來源、驗收 pass/fail、整合影響評估 |
| 規格與視圖 | `design simulation capability` | `<spec>`、介面、視圖需求 | 規格文件/視圖產物、版本/可追溯性 |
| 串擾與電性 | `design simulation capability` / `test/SOP capability` | 耦合條件、量測/模擬設定 | 結果、門檻比較、證據 |
| SOP/生產/測試 | `test/SOP capability` | 製程/量測/驗收需求 | SOP、測試紀錄、追溯欄位 |
| 交付與 KPI 閘門 | `acceptance/KPI gate capability` | KPI、驗收標準、交付包 | 證據齊全、pass/fail、不可未達標宣稱完成 |
| 工具與流程 | `index/orchestration capability`（本身）/通用工程能力 | 重構、部署、文件化、技能生成 | 變更記錄、驗證證據 |

## 路由規則（D1/R2）
- 先依使用者任務選擇 capability/子域，再依專案可用實作執行。
- 子能力可交回 `acceptance/KPI gate capability` 裁決；狀態不明或缺證據 → stop-the-line（見 C1）。
- 規範不綁定 sibling skill ID；專案可在 1b 範例中映射到具體模組/skills。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Delivery/KPI gate、Evidence 最小欄位、Stop-the-line、Change control、受控 capability 詞彙。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。
- 專案可能包含設計模擬、熱負載、元件整合、材料資料、SOP/生產、KPI 交付驗收等具體 skills/模組；名稱與路徑依 `<workspace>`。公开標準（單位、通用 SOP 結構）可保留；專有數值依 6B。
