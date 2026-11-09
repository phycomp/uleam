# 技能清單暨使用情境 (Skills Index)

## 一、程式化技能（generated_skills/）

| 技能 | 目錄 | 使用情境 |
|------|------|----------|
| notifier | generated_skills/notifier | 多通道通知（SMS/Email），fallback 與 Repo 舊介面相容 |
| greeter | generated_skills/greeter | 範本技能，示範 skill-generator 產出結構 |
| impedance_calculator | generated_skills/impedance_calculator | 計算量子傳輸線阻抗（超導修正） |
| thermal_load | generated_skills/thermal_load | 計算熱負載（固體熱傳導 + 衰減器） |
| cross_section_renderer | generated_skills/cross_section_renderer | 解析截面 AST 為幾何多邊形 |
| agent_workflow | generated_skills/agent_workflow | 執行代理人狀態機優化循環 |
| dsl_parser | generated_skills/dsl_parser | CSV→AST 與截面解析 |

## 二、OpenCode 技能（.agents/skills/）

| 技能 | 目錄 | 使用情境 |
|------|------|----------|
| skill-generator | .agents/skills/skill-generator | 依 Spec+Repo AST+Policy 生成技能 |
| generic-qcable | .agents/skills/generic-qcable | 通用型量子傳輸線設計/計算/優化/重構 |
| component-integration | .agents/skills/component-integration | 衰減器/LPF/IR Filter 整合 |
| thermal-load-measurement | .agents/skills/thermal-load-measurement | 低溫熱負載量測 |
| thermal-load-simulation | .agents/skills/thermal-load-simulation | 熱負載模擬與計算 |
| thermal-load-units | .agents/skills/thermal-load-units | 熱負載單位與轉換 |
| thermal-load-sop | .agents/skills/thermal-load-sop | 熱負載量測 SOP |
| nbtii-small-batch | .agents/skills/nbtii-small-batch | NbTi 小量生產 |
| nbtii-pcb-fab | .agents/skills/nbtii-pcb-fab | 板廠單位/DFM/驗收 |
| nbtii-medium-batch | .agents/skills/nbtii-medium-batch | 中量生產 |
| nbtii-r2r-mass | .agents/skills/nbtii-r2r-mass | R2R 大量生產 |
| nbtii-test-sop | .agents/skills/nbtii-test-sop | 生產測試 SOP |

## 三、核心模組（根目錄 .py）

| 模組 | 使用情境 |
|------|----------|
| 計算.py | 物理計算核心（阻抗/熱負載/微帶線） |
| 疊構Util.py | 截面解析器（介電/導體/盲孔） |
| 代理主程式.py | 代理人狀態機 |
| 元件整合.py | 衰減器/LPF/IR filter 模型 |
| 掃瞄器.py / ast_scanner.py | Repo AST 掃描 |
| orchestrator.py | SKILL 產生器 CLI（OpenAI 版） |
| app.py | Streamlit 統一入口 |