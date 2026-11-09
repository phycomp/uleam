---
name: nbtii-pcb-fab
description: Use when the user needs outsourced PCB/flex fabrication specs, DFM checks, or vendor acceptance criteria for precision/cryogenic transmission-line builds, and asks to 板廠、PCB fab、DFM、委外製造、外包驗收.
---

# Fabrication/Vendor Spec & DFM Capability（可移植）

本 skill 提供**委外製造規格、DFM 與驗收**結構。規範用中性佔位（6B）；公開 DFM/SOP 結構可保留。

## 規格/DFM（範本）
- 材料/疊構、線寬線距、公差、孔/鍍層、表面處理、可製造性限制（對齊 `<spec>` 與廠商能力）。
- 拼板、對位、標記、清潔與包裝要求。
- 關鍵風險：公差疊加、材料/環境相容、可測性。

## 驗收（範本）
- 尺寸/外觀、電性/阻抗或指定測試、必要時環境/低溫抽樣；證據與追溯完整。
- 不合格隔離、讓步需明確記錄且不得違反必要 `<kpi_id>` 門檻。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。缺證據或未達必要門檻不得宣稱驗收通過。

## 交棒（capability）
- 設計 → `design simulation capability`；材料 → `material/component data capability`；測試 → `test/SOP capability`；裁決 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。具體廠商、材料牌號、內部公差與報價流程依 6B/專案。