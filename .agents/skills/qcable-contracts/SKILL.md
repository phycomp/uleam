---
name: qcable-contracts
description: Use when a quantum-cable or engineering delivery skill needs stable cross-skill contracts for KPI/delivery gates, acceptance evidence, stop-the-line rules, or controlled capability routing, or asks to 契約、KPI 閘門、驗收證據、交付階段、不達標不可宣稱完成、capability routing、能力圖.
---

# QCable / Engineering Contracts（stable, C1a）

本文件提供**共用契約**，供量子線纜/工程交付叢集的 skills 以 D1/R2 方式引用。規範文字使用中性佔位（6B）；公開標準（如物理單位、通用 SOP 結構）可保留；專有/內部數值僅可置於非規範 1b 範例且經明確允許。

## Contract Reference (stable) — Delivery/KPI Gate
- **Stages (capability flow, not skill IDs)**：`spec/KPI definition` → `development/design` → `test/measurement` → `verification` → `delivery` → `usage+test+data records` → `acceptance/KPI gate`。
- **Gate rule**：僅當所需證據存在且適用的 KPI/驗收準則通過時，才可宣稱階段/交付物完成。缺證據、結果不可讀、或未達門檻 → **不得宣稱完成**；回到負責的 capability 修正並重新驗證。
- **Evidence (minimum fields, portable)**：`<artifact_id|kpi_id>`、subject/slug、stage、method/command 或 procedure ref、expected threshold/criteria、observed result、pass/fail、timestamp、owner/context、evidence path 或 record ref。需可追溯、可複核。
- **Stop-the-line**：量測/狀態不明、追溯缺失、閘門失敗、交付狀態未驗證 → 記錄證據並停止；不得假成功、不得盲目重試。
- **Change control**：契約/schema/KPI 定義變更需版本化，並在下游閘門依賴前重新驗證。

## Capability Routing Vocabulary (controlled, minimal)
- `design simulation capability`
- `material/component data capability`
- `test/SOP capability`
- `integration capability`
- `acceptance/KPI gate capability`
- `index/orchestration capability`

子 skill 可用上述通用 capability 名稱交棒（**不綁 sibling skill ID**）。Index/orchestration 類可保留**受控 capability/子域名稱**列舉與能力圖；規範判定仍引用本契約。

## Reference implementation (non-normative example, 1b)
> 量子線纜/NbTi/熱負載/電性/交付叢集的專案 skills 可作為參考實作。具體路徑、內部門檻、批次/廠商/機密參數不作為規範；若出現，依 6B 僅能放在明確標註的非規範範例中。 مثال