---
name: hierarchy-visualization
description: "層級視覺化技能：分析技能上下層級與 repo 代碼依賴，輸出文字樹/Mermaid/JSON。Use when the user wants to visualize hierarchy, analyze skill/repo dependencies, or generate dependency graphs."
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---
# Hierarchy Visualization — 層級視覺化

## 來源
本地實作（yogsoth-ai/hierarchy-visualization 為私有 repo，無法安裝）。

## 功能
- `examples/skill_viewer.py --parent <name>`：列出下層級（文字/JSON）。
- `examples/skill_viewer.py --tree`：完整層級樹。
- `examples/hierarchy_analyzer.py`：repo import graph + Mermaid 輸出。

## 使用
```bash
cd /home/sam/代理人
python examples/skill_viewer.py --parent generic-qcable --json
python examples/hierarchy_analyzer.py --format mermaid --output docs/HIERARCHY_MERMAID.md
python examples/hierarchy_analyzer.py --repo /path/to/repo --format json
```

## 與 skill-hierarchy-viewer 的比較
- hierarchy-visualization：本地實作，輸出 text/mermaid/json。
- skill-hierarchy-viewer：技能封裝，含 HIERARCHY 映射與使用情境。

## 觸發條件
- 「層級視覺化」「hierarchy visualization」「依賴圖」「技能層級」
