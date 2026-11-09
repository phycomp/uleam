---
name: refactor
description: Use when the user wants to restructure/integrate a large multi-module project, needs decision-node questioning before implementation, phased migration, and verification/evidence at each phase, and asks to 重構、整合、遷移計畫、決策節點、分階段重構.
---

# Restructure & Integration Capability（可移植）

本 skill 提供**大型多模組專案重構/整合**流程：實作前詰問決策節點、分階段遷移、並行降低風險、每階段驗證與證據。規範用中性佔位（6B）；公開工程/SOP 結構可保留。

## 核心原則
1. **實作前詰問**：每輪聚焦少量決策節點（選項化），避免模糊開工。
2. **決策節點記錄**：問題→選項→決策→理由/影響，形成可追溯表。
3. **分階段遷移**：骨架/介面 → 範例遷移 → 批次遷移 → 封存/清理；每階段可驗證。
4. **並行與相容**：優先保留相容/橋接策略降低風險；刪除舊結構前確認無依賴並有證據。
5. **測試與證據同步**：靜態檢查、單元/整合/smoke（依專案）與變更證據；**未驗證不得宣稱完成**。
6. **文件沉澱**：使用/測試/限制/遷移狀態隨階段更新。

## 工作流程（範本）
- **盤點**：結構、模組、依賴、既有測試/文件、風險。
- **詰問**：交付形態、範圍、相容策略、資料/狀態、測試/部署、命名/結構、可觀測性等。
- **決策表**：固化決策；未決事項標註阻塞。
- **Phase 0**：最小可運行骨架 + 驗證。
- **Phase 1+**：按優先序遷移核心/高價值模組；每階段 commit/checkpoint + 證據。
- **封存/清理**：在依賴解除且驗證通過後進行。
- **驗收**：交由 `acceptance/KPI gate capability` 依 C1 裁決。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line、Change control。遷移/介面變更屬 change control；狀態不明或驗證失敗不得宣稱完成。

## 交棒（capability）
- 領域設計/計算 → `design simulation capability`；測試/SOP → `test/SOP capability`；資料 → `material/component data capability`；整合 → `integration capability`；裁決 → `acceptance/KPI gate capability`；選路 → `index/orchestration capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。`<workspace>` 可能為 Web/UI、多頁應用、Python 套件或混合專案；具體目錄、語言、框架、指令與路徑依 6B/專案。公開工具（版本控制、測試框架、格式檢查）可依實際環境選用。