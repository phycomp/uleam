# 功能清單 (Feature Inventory)

## 核心計算
- 超導阻抗計算（London penetration depth + 動態電感修正）
- 熱負載耦合計算（固體熱傳導 + 衰減器自發熱）
- 微帶線快速阻抗/損耗估算（IPC-2141）
- 量子傳輸線多場耦合 AI Agent（電性-熱負載迭代優化）

## 截面與 DSL
- 通用型截面 DSL 向量渲染器（YAML/JSON AST）
- CSV → AST → 向量多邊形渲染 Pipeline
- 疊構解析器（介電/導體/盲孔幾何）
- PCB 多層堆疊渲染（11 層）
- FPC 疊構自動化編譯與渲染

## DSL 產生器
- Ansys PyAEDT 元件解析工廠
- PyAnsys 腳本產生器
- 傳輸線截面 DSL 語法樹產生器

## 代理人 / 狀態機
- 純 Python 狀態機（Init/ElecCalc/ThermalCalc/Review/Generator）
- 多目標優化（Optuna/Pareto）
- RL 閉環優化（PPO）
- 代理模型（GradientBoosting）+ LLM 輔助

## SKILL 產生器
- OpenCode/BEAM 化 skill（`.agents/skills/skill-generator/`）
- AST 掃描器（`掃瞄器.py` / `ast_scanner.py`）
- Gatekeeper 審查 + Adapter 分析 + 程式碼/測試生成

## 元件整合
- 衰減器自發熱模型
- LPF 截止頻率與衰減
- IR filter 傳輸模型
- `元件整合.py`：整合入口 `integrate_components(spec)`
- 技能：`component-integration`

## 已產出技能（generated_skills/）
- notifier、greeter、impedance_calculator、thermal_load、cross_section_renderer、agent_workflow、dsl_parser

## UI 入口
- `app.py`：Streamlit 統一導覽
- `pages/`：多頁面（阻抗計算、DSL 描述、自動化分析、N 通道 S 參數、通用截面、Ansys 產生器、PCB 渲染、FPC 截面）

## 工具與文件
- `examples/run_example.py`、`examples/test_example.py`
- `docs/USAGE_FLOW.md`、`docs/FEATURES.md`
- `REFACTOR_MANIFEST.md`：重構決策與進度