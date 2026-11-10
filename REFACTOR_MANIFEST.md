# 重構整合清單 (Refactor Manifest)

## 決策節點
- 範圍：A1 全部模組
- 版本策略：B1 備份後合併（舊版移至 archive/）
- 入口：C1 Streamlit 多頁（app.py 統一導覽）

## 已執行
- archive/計算舊.py（舊版，無引用）
- 疊構Util.py：`疊構解析` 統一指向 `疊構解析II`
- pages/01主程式.py：移除重複 import
- app.py：統一 Streamlit 導覽入口

## 已執行（續）
- 圖結構.py / 定時.py / 計算阻抗.py：修正語法錯誤，全專案可 compile
- 計算.py：補上 numpy import
- 代理主程式.py：改寫為純 Python 狀態機（移除 langgraph 依賴），保留 app.invoke 介面
- ast_scanner.py：shim，orchestrator 可直接 import
- .agents/skills/skill-generator/：OpenCode/BEAM 化 skill（SKILL.md + prompts）

## 待處理（下一決策節點）
- 計算.py / 計算阻抗.py / 計算阻抗II.py 職責釐清與合併
- pages/01主程式.py vs 01主程式II.py 功能差異合併
- 代理人/ 目錄與 .md/.pdf 文件整理
- 06/07 系列確認非重複（功能不同），保留雙版本
- 計算.py / 計算阻抗II.py：將 `calc_microstrip_qubit` 合併入 `計算.py`，pages/09 改為 import
- 疊構Util.py：移除重複的 `疊構解析` 實作，統一委派至 `疊構解析II`
- generated_skills/notifier/：skill-generator 範例產出（notifier.py + test_notifier.py）
- generated_skills/greeter/：skill-generator 範本產出（greeter.py + test_greeter.py）
- generated_skills/impedance_calculator/、thermal_load/、cross_section_renderer/：skill-generator 產出（計算/分析類）
- generated_skills/agent_workflow/、dsl_parser/：skill-generator 產出（代理人/DSL 類）
- docs/：移入代理人敘述型 .md 文件；新增 USAGE_FLOW.md（執行/測試/使用流程）
- examples/：新增 run_example.py、test_example.py
- .agents/skills/generic-qcable/：抽象化 quantum-cryogenic-cable 為通用型量子傳輸線技能
- ~/.opencode/skills/：全域佈署 mantaro、polar 及全部 .agents/skills
- .agents/skills/component-integration/：元件整合技能
- 元件整合.py：衰減器/LPF/IR filter 模型
- docs/FEATURES.md：功能清單
- docs/SKILL_AUDIT.md：量子傳輸線技能盤點與整合狀態
- docs/SKILLS_INDEX.md、docs/TEST_GUIDE.md、docs/USAGE.md：技能清單/測試指南/使用說明
- docs/TEST_REPORT.md、docs/EXAMPLES.md：測試報告與範例（整合 anatask-pstack-impl）
- docs/KPI_COMPLIANCE.md：KPI 需求比對報告
- docs/KPI_PIPELINE.md：KPI 規格平台完整 Pipeline
- kpi_platform/：KPI 驗收/驗證/追蹤模組
- examples/test_kpi_pipeline.py：KPI pipeline 測試
- examples/test_mantaro_polar.py：mantaro/polar 技能測試
- .agents/skills/cloud-deploy/：雲端佈署與驗證技能
- .agents/skills/qcable-index/、connector/、three-view/：技能索引、連接器、三視圖技能
- .agents/skills/channel-manager/：頻道管理技能
- 頻道管理.py：頻道管理模組
- content_templates/：內容主題模板（quantum/sciedu/PQC）
- crontab_example.txt：排程範例
- .agents/skills/kpi-delivery-valid/：KPI 交付驗證 Pipeline 技能
- .agents/skills/engineering-delivery/：通用工程開發→驗收 Pipeline 技能
- .agents/skills/material-db/：材質數據庫技能
- 材質數據庫.py：材質數據庫模組
- .agents/skills/crosstalk-calc/、electrical-spec/、electrical-test-sop/：串擾計算、電性規格、電性測試 SOP
- kpi_platform/：KPI 規格平台（物理公式、驗證、追蹤）
- pages/10KPI平台.py：KPI 規格平台 UI
- .agents/skills/llm-parser/、measurement-unit-link/：LLM 解析、量測單位鏈結
- LLM解析.py：LLM 自然語法解析模組
- 串擾計算.py：串擾計算模組
- docs/SKILL_HIERARCHY.md：技能層級架構
- docs/SKILL_HIERARCHY_FULL.md：完整技能層級（含 YouTube/Git）
- docs/QUANTUM_MARKET_ANALYSIS.md：量子市場分析報告
- docs/HIERARCHY_MERMAID.md：Mermaid 層級圖
- examples/hierarchy_analyzer.py：層級分析工具
- 三視圖.py：三視圖模組（前/側/上，獨立函式）
- docs/CLOUD_SETUP.md：雲端佈署指南
- Dockerfile、wrangler.toml、worker.js、requirements.txt、.github/workflows/deploy-cloudflare.yml：佈署設定
- .agents/skills/：新增 9 個技能（thermal-load-* ×4、nbtii-* ×5）
- docs/：移入 5 個 .pdf 二進位文件，根目錄減肥
