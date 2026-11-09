---
name: nbtii-small-batch
description: Use when the user needs a small-batch/prototype fabrication workflow for superconducting or precision transmission-line builds (materials prep, patterning/stack steps, inspection, basic electrical/cryogenic checks), and asks to 小量生產、原型製作、prototype fabrication、lab-scale batch.
---

# Small-Batch / Prototype Fabrication Capability（可移植）

本 skill 提供**小批量/原型製程**的結構化流程。規範用中性佔位（6B）；公開單位與通用製程/SOP 結構可保留。

## 適用
- 原型驗證、研究、小批量（`<batch_size>` 小）；目標是建立可追溯製程與初步證據。

## 流程（範本）
1. 材料/基材/元件準備：`<material>`, `<stackup>`，來源可追溯。
2. 圖形/層結構製作：依 `<spec>` 與製程能力；關鍵尺寸記錄。
3. 組裝/整合：介面與元件整合（交由 `integration capability`）。
4. 檢查：外觀/尺寸/基本電性；必要時低溫/環境抽樣（交由 `test/SOP capability`）。
5. 記錄：批次/樣品、參數、結果、異常與處置（對齊 C1 Evidence）。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line。關鍵檢查未完成/追溯缺失不得宣稱樣品合格。

## 交棒（capability）
- 設計/規格 → `design simulation capability`；材料 → `material/component data capability`；測試/SOP → `test/SOP capability`；裁決 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。具體材料體系（如 NbTi 類）、製程設備、內部門檻與實驗室路徑依 6B/專案。