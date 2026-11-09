# CrewAI vs AutoGen vs LangGraph 比較與選型

## 總覽

| 維度 | CrewAI | AutoGen | LangGraph |
|---|---|---|---|
| 範式 | 角色導向 Crew/Agent/Task | 對話式多代理 (GroupChat) | 狀態圖 StateGraph (Nodes/Edges) |
| 抽象層級 | 高 (快速上手) | 中 (對話驅動) | 低 (顯式控制流) |
| 控制流 | Sequential / Hierarchical | 彈性對話 | 條件邊、循環、分支 |
| 狀態管理 | 隱式 (任務上下文) | 對話歷史 | Typed State + Checkpointing |
| 工具呼叫 | @tool 裝飾器 | Function calling | ToolNode / bind_tools |
| 本地 LLM (Ollama) | 支援 (ollama/...) | 支援 (OpenAI 相容) | 支援 (langchain-ollama / OpenAI 相容) |
| 學習曲線 | 低 | 中 | 高 |
| 確定性 | 中 | 低 (對話驅動) | 高 (圖結構) |
| 最佳用途 | 快速多代理管線 | 研究/探索/對話 | 複雜有狀態工作流 |
| 適合本專案 | 角色定義 (Researcher/Optimizer/...) | 不採用 | 編排/狀態/Checkpointing |

## 本專案選型決策

**採用：LangGraph 編排 + CrewAI 角色 (混合)**

理由：
1. 現有程式碼 (`決策節點與優化.py`) 已使用 LangGraph `StateGraph`/`AgentState`，延續性高。
2. skill.md 要求「確定性工具 + LLM 僅參數提取/決策」，LangGraph 的顯式節點/邊最能保證此約束。
3. 需要 SQLite checkpointing (可恢復、人機迴圈、除錯重播)，LangGraph 原生支援 `SqliteSaver`。
4. CrewAI 提供高階角色抽象 (role/goal/backstory)，適合定義 Researcher/Optimizer/Guardrail/Reporter 角色，嵌入 LangGraph 節點。

## 決策節點

### 節點 1：框架選型
- 選項：CrewAI / AutoGen / LangGraph / 混合
- 決策：**混合 (LangGraph + CrewAI)**
- 理由：控制流確定性 + 角色抽象兼具。

### 節點 2：整合範圍
- 選項：新增層 / 全面重構 / PoC
- 決策：**全面重構為 Agent-First** (分階段實作建議被拒絕，採一次性)

### 節點 3：本地模型
- 硬體：RTX 5060 8GB VRAM, 15GB RAM
- 決策：**Llama3 8B Q4 (Ollama)**，VRAM ~4.7GB，推理可互動

### 節點 4：Agent 角色
- 決策：**全部 5 角色** (Optimizer, Physicist/Calculator, Guardrail, Reporter, Researcher)

### 節點 5：部署端點
- 原始目標：Ollama + Llama3
- 決策：**Ollama + Llama3 8B** (port 11434)，OpenAI 相容端點

### 節點 6：可觀測性
- 決策：**Streamlit 新增 Agent Trace 頁面**，顯示每輪決策節點/工具呼叫/狀態

### 節點 7：持久化
- 決策：**SQLite checkpointer** (SqliteSaver)

### 節點 8：工具層
- 決策：**確定性工具包裝** (LLM 不心算物理)，符合 skill.md guardrail

## 建議 (Advice)

1. 全面重構工程量大，建議至少保留確定性工具層不變，僅替換 LLM 大腦為 Agent 編排。
2. 本地 8B 模型推理約 3-8 秒/次，10 輪優化約 1-2 分鐘；UI 需顯示進度。
3. 若未來需要 70B 品質，需 CPU offload 或更大 VRAM (≥48GB)。
4. CrewAI 角色僅用於 Researcher/Reporter (自然語言)，Optimizer/Guardrail/Physicist 保持確定性，避免 LLM 決策不穩定。