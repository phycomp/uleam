# 使用流程說明 (Usage Flow)

## 1. 整體工作流程

```
掃瞄目錄夾 → 建立決策節點（反覆詰問）→ 實作 → 測試 → skill-generator 產出技能
```

### 步驟 A：掃瞄目錄夾
```bash
cd /home/sam/代理人
python -c "from 掃瞄器 import scan_repo; import json; print(json.dumps(scan_repo('.'), ensure_ascii=False, indent=2)[:2000])"
```
產出 Repo AST 摘要，作為後續決策基礎。

### 步驟 B：建立決策節點
使用 `question` 工具反覆詰問使用者，每個問題結束前給予建議。決策節點涵蓋：
- 範圍（全部/核心/截面）
- 版本策略（備份後合併/刪除/deprecated）
- 入口形式（Streamlit/CLI/雙軌）
- LLM 後端（OpenAI / 本地 / OpenCode+BEAM）

### 步驟 C：實作與重構
- 統一入口：`app.py`（Streamlit navigation）。
- 解析器整合：`疊構Util.py`（`疊構解析` → `疊構解析II`）。
- 狀態機：`代理主程式.py`（純 Python，無 langgraph 依賴）。
- 計算模組：`計算.py`（含 `calc_microstrip_qubit`）。

### 步驟 D：測試
```bash
cd /home/sam/代理人
python examples/test_example.py          # smoke tests
python generated_skills/<skill>/test_*.py  # 單一技能測試
```

### 步驟 E：skill-generator 產出技能
1. 準備 Spec（如 `spec_notifier.md`）。
2. 掃描 Repo AST。
3. Gatekeeper 審查 → 衝突/Adapter 分析 → 程式碼生成 → pytest 生成 → 落盤。
4. 產出位於 `generated_skills/<skill_name>/`。

OpenCode 化 skill 位於 `.agents/skills/skill-generator/`，可由 BEAM 直接執行，不需 OpenAI API key。

## 2. 執行範例
```bash
cd /home/sam/代理人
python examples/run_example.py
```
示範：阻抗計算、熱負載、截面解析、Greeter、Notifier、DSL Parser、Agent Workflow。

## 3. 測試範例
```bash
cd /home/sam/代理人
python examples/test_example.py
```
彙總所有技能的 smoke tests。

## 4. 主要檔案索引
| 檔案 | 說明 |
|------|------|
| `app.py` | Streamlit 統一入口 |
| `計算.py` | 核心物理計算模組 |
| `疊構Util.py` | 截面解析器 |
| `代理主程式.py` | 代理人狀態機 |
| `ast_scanner.py` | 掃描器 shim |
| `orchestrator.py` | SKILL 產生器 CLI（OpenAI 版） |
| `.agents/skills/skill-generator/` | OpenCode/BEAM 化 SKILL 產生器 |
| `generated_skills/` | 產出的技能 |
| `examples/` | 執行/測試範例 |
| `docs/` | 文件與 PDF |
| `archive/` | 歸檔的舊版檔案 |
| `REFACTOR_MANIFEST.md` | 重構決策與進度 |