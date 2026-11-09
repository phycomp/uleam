---
name: polar
description: Use when the user wants to generate sampling plans for field-solver/oracle training data (geometry/stackup parameter sweeps, CSV outputs for external solver results), or asks to 採樣計畫、sampling plan、oracle 訓練資料、參數掃描、solver CSV.
---

# Sampling Plan / Oracle Data Capability（可移植）

本 skill 產生**參數掃描/採樣計畫**供外部求解器或資料集建立。規範用中性佔位（6B）。

## 流程
1. 定義模板/目標（`<target_metric>`）、變數與範圍/因子。
2. 產生可追溯 case 清單（case id、參數、單位、模型/模板 ref），預留結果欄位。
3. 外部求解/量測結果回填後，作為資料集需標註來源、版本與驗證狀態。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：資料/結果若用於驗收或模型決策，需 Evidence/追溯；來源不明 stop-the-line。

## 交棒（capability）
- 設計/模擬 → `design simulation capability`；驗證/裁決 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。`<workspace>` 可能包含模板載入與 CSV 產生腳本；具體路徑、目標值與因子依 6B。