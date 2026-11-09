---
name: engineering-delivery
description: Use when the user wants a generic engineering development-to-acceptance pipeline (KPI/spec to delivery) for any product domain, needs per-stage verification/evidence guidance, or asks to 工程交付、開發到驗收、KPI pipeline、spec→delivery、驗證證據、各階段驗收.
---

# Engineering Delivery Capability（可移植）

本 skill 提供**跨領域工程交付**流程（不限產品類型），與 `qcable-contracts`（C1）一致。規範用中性佔位（6B）；公開標準可保留。

## Capability Flow
`spec/KPI definition` → `development/design` → `test/measurement` → `verification` → `delivery` → `usage+test+data records` → `acceptance/KPI gate`

## 階段指引（最小可攜）
1. **Spec/KPI**：定義功能/性能/可靠性/SOP/第三方驗證等 `<kpi_id>` 與門檻；版本化。
2. **Development/design**：模組與介面可追溯；風險/假設記錄。
3. **Test/measurement**：可重現的測試/量測；保留命令、環境、原始輸出或記錄 ref。
4. **Verification**：以證據比對門檻；「可執行/可編譯」不等於通過。
5. **Delivery**：交付包含使用說明、測試/驗證證據、已知限制；不得隱瞞未驗證項。
6. **Records**：使用+測試+資料/材料/參數記錄可追溯。
7. **Acceptance/KPI gate**：各必要 KPI 通過才可宣稱交付完成；否則回修並重驗。

## 證據與文件（可裁剪）
- Usage/操作說明、測試報告（環境、pass/fail、證據）、範例/情境。
- 已知限制必須列出未驗證步驟與原因。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Delivery/KPI gate、Evidence 最小欄位、Stop-the-line、Change control、controlled capability routing。索引/編排可用 capability/subdomain map，不綁 skill ID。

## 交棒（capability）
- 設計/模擬 → `design simulation capability`
- 材料/元件/參數資料 → `material/component data capability`
- 測試/SOP → `test/SOP capability`
- 整合 → `integration capability`
- 裁決 → `acceptance/KPI gate capability`
- 選路 → `index/orchestration capability`

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。
- 可對應不同領域（軟體、硬體、製程、量測系統等）；`<workspace>` 內的具體模組、門檻、廠商/批次/內部參數依 6B。
