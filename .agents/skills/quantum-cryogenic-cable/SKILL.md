---
name: quantum-cryogenic-cable
description: Use when the user wants to design, calculate, or optimize a cryogenic/quantum transmission line from a spec (impedance, thermal load, views, crosstalk), or asks to 低溫/量子傳輸線、阻抗、熱負載、三視圖、串擾、規格計算、cryo cable design.
---

# Cryogenic/Quantum Transmission-Line Capability（可移植）

本 skill 聚焦**低溫/量子傳輸線**的設計與計算能力，適用於使用者提供的 `<spec>`（不綁定固定產品代號）。規範用中性佔位（6B）；公開單位與通用低溫/傳輸線工程概念可保留。

## 決策點
1. **規格與溫區**：明確 `<spec>`、`<temperature_stage>`/工作條件、介面與目標 `<kpi_id>`（阻抗、損耗、熱負載、串擾、可靠性等）。
2. **模型與假設**：材料/幾何/邊界條件假設必須可追溯；低溫物性來源需標註（交由 `material/component data capability` 或記錄）。
3. **計算 vs 量測 vs 驗收**：計算/模擬由 `design simulation capability` 輸出；量測/SOP 由 `test/SOP capability`；達標裁決由 `acceptance/KPI gate capability`（C1）。
4. **整合影響**：衰減/濾波/熱管理/連接等元件交由 `integration capability` 與對應資料/SOP 能力。

## 規格欄位（中性範本）
| 欄位 | 說明 | 佔位 |
|---|---|---|
| channel count | 通道數 | `<channel_count>` |
| pitch/spacing | 間距 | `<pitch>` |
| conductor geometry | 導體/線寬/厚度 | `<geometry>` |
| dielectric/stackup | 介電與疊構 | `<stackup>` |
| conductor/dielectric material | 材料類別/參考 | `<material>` |
| temperature stages | 溫區/熱錨點 | `<temperature_stage>` |
| targets | 阻抗/熱負載/串擾/損耗等 | `<targets>` / `<kpi_id>` |

## 能力子域（受控）
- **阻抗/幾何/規格轉換**：依可追溯模型與參數計算。
- **熱負載**：溫區/材料/幾何假設下的估算與敏感性；單位明示（公開 SI 單位可用）。
- **視圖/佈局輔助**：用於溝通與製造/整合檢視；非驗收證據除非另有量測/檢驗記錄。
- **串擾/電性**：耦合條件下估算或與量測比對；需標註方法與條件。
- **優化（可選）**：多目標搜尋須在可追溯約束下進行；結果交驗證/閘門。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：
- Gate rule：未達門檻/缺證據不得宣稱完成。
- Evidence：`<kpi_id|artifact_id>`、規格/條件、方法/模型/命令、expected vs observed、pass/fail、timestamp、record ref。
- Stop-the-line：狀態不明、來源不可追溯、關鍵假設缺失、閘門失敗 → 停止並記錄。
- Capability routing：`design simulation capability` / `material/component data capability` / `test/SOP capability` / `integration capability` / `acceptance/KPI gate capability` / `index/orchestration capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。
- `<workspace>` 可能包含低溫/傳輸線核心計算模組、熱負載模型、視圖、串擾/優化與 UI；具體產品代號、路徑、材料牌號、內部門檻與參數依 6B。