---
name: skill-hierarchy-viewer
description: "技能層級檢視器：分析技能上下層級與 repo/skills 依賴，支援文字樹、Mermaid、JSON 輸出，並與 hierarchy-visualization 比較。Use when the user wants to view skill hierarchy, analyze repo/skill dependencies, or export hierarchy as JSON/Mermaid."
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---
# Skill Hierarchy Viewer — 技能層級檢視器

## 功能
1. **層級分析**：指定上層級，列出下層級（文字/JSON）。
2. **完整層級樹**：`--tree` 印出所有根節點的依賴樹。
3. **Repo/Skills 分析**：掃描 repo 的 import 依賴 + skills 的 HIERARCHY 映射。
4. **輸出格式**：text / mermaid / json。

## 使用
```bash
cd /home/sam/代理人
# 列出 generic-qcable 的下層級（文字）
python examples/skill_viewer.py --parent generic-qcable
# JSON 格式
python examples/skill_viewer.py --parent generic-qcable --json
# 完整層級樹
python examples/skill_viewer.py --tree
# Mermaid 層級圖
python examples/hierarchy_analyzer.py --format mermaid --output docs/HIERARCHY_MERMAID.md
# Repo import graph
python examples/hierarchy_analyzer.py --repo /home/sam/代理人 --format json
```

## 與 hierarchy-visualization 的比較
| 項目 | skill-hierarchy-viewer | hierarchy-visualization |
|------|------------------------|------------------------|
| 輸出格式 | text / mermaid / json | 互動式 HTML / 圖 |
| 依賴來源 | HIERARCHY 映射 + repo import 掃描 | AST/模組分析 |
| 適用 | 技能層級 + Python repo | 任意程式碼庫架構 |
| 安裝 | 本地腳本 | `npx skills add` |

- **skill-hierarchy-viewer**：適合技能生態系的層級檢視，支援 JSON/Mermaid 輸出，可整合至 CI/CD。
- **hierarchy-visualization**：適合任意程式碼庫的互動式架構圖，支援多層展開。

## 觸發條件
- 「技能層級」「skill hierarchy」「上下層級」「repo 依賴」「hierarchy viewer」