---
name: generic-qcable
description: Use when the user wants to design, calculate, or optimize a transmission line or cryogenic/quantum cable from user-provided specs (impedance, thermal load, views, crosstalk), run multi-objective optimization workflows, or restructure/integrate a multi-module engineering project, and asks to 傳輸線設計、規格計算、熱負載、三視圖、串擾、優化、重構整合.
---

# Generic Transmission-Line Design & Optimization Capability（可移植）

本 skill 提供**通用傳輸線/低溫線纜設計、計算、優化與重構整合**能力。規格由使用者提供（不綁定特定產品代號）；規範用中性佔位（6B）。公開可引用標準（單位、通用公式/模型結構）可保留。

## 決策點
1. **規格是否完整？** 至少明確 `<spec>` 關鍵欄位（通道/幾何/材料類別/介面/溫區或工作條件/目標指標）；缺項列為假設並標註。
2. **計算/模擬 vs 驗收裁決**：本能力可產出計算/模擬結果與建議；是否達標由 `acceptance/KPI gate capability` 依 `qcable-contracts`（C1）裁決。
3. **資料/材料來源**：材料屬性、元件參數交由 `material/component data capability` 或具來源的記錄；不可追溯假設不得作為通過證據。
4. **測試/SOP**：量測、製程、試驗程序交由 `test/SOP capability`；本能力輸出可作為驗證輸入。
5. **整合**：堆疊/元件整合影響交由 `integration capability` 協同評估。

## 規格欄位（中性範本）
| 欄位 | 說明 | 佔位 |
|---|---|---|
| channels / count | 通道數或導體數 | `<channel_count>` |
| pitch / spacing | 間距 | `<pitch>` |
| line/trace geometry | 線寬/厚度/幾何 | `<geometry>` |
| dielectric/stackup | 介電/疊構參數 | `<stackup>` |
| material class | 導體/介電/結構材料類別 | `<material>` |
| operating conditions | 溫區/頻段/功率/環境 | `<conditions>` |
| target metrics | 阻抗、損耗、熱負載、串擾等 `<kpi_id>` | `<targets>` |

## 能力子域（受控）
- **設計計算**：阻抗/幾何關係、傳輸參數、視圖/佈局輔助（依專案模型）。
- **熱分析**：熱負載估算、溫區假設、敏感性（單位明示；模型/假設可追溯）。
- **串擾/電性**：耦合/串擾、電性指標估算；與量測/驗證比對時交由 test/verification 流程。
- **多目標優化（可選）**：在可追溯目標與約束下搜尋參數（如貝葉斯/代理模型/RL/啟發式/LLM 輔助參數生成）；優化結果仍需驗證，**不可未驗證宣稱達標**。
- **重構整合（可選）**：多模組專案可採決策節點→可驗證單位→證據回報的漸進整合；引用 C1 的 stop-the-line 與證據欄位。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：
- **Delivery/KPI gate**：階段 flow 與 gate rule 適用；未達門檻/缺證據不得宣稱完成。
- **Evidence**：規格、假設、模型/命令、輸入參數、輸出、與 `<kpi_id>` 門檻比較、pass/fail、evidence ref。
- **Stop-the-line**：模型/資料/狀態不明、關鍵假設未標註、驗證缺失 → 停止並記錄。
- **Capability routing**：材料/元件 → `material/component data capability`；測試/SOP → `test/SOP capability`；整合 → `integration capability`；裁決 → `acceptance/KPI gate capability`；選路 → `index/orchestration capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。
- `<workspace>` 可能包含領域計算模組（熱/電/視圖/串擾）、規格轉換、UI/流程腳本、優化與代理模型實驗程式。具體規格代號、路徑、模型參數、門檻值與內部實作依 6B/專案設定；公開單位與通用工程概念可保留。