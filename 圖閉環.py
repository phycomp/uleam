import os
import json
import re
from typing import Annotated, List, Dict, Any, Literal
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic

# 導入官方 MCP 適配器，將 MCP 工具無縫轉化為 LangGraph 看得懂的格式
from langchain_mcp_adapters.client import mcp_server_tools_stub

# =====================================================================
# 1. 狀態定義 (State) - 支援超長上下文與持久化
# =====================================================================
class ClientAgentState(TypedDict):
    # 支援 LangGraph 原生訊息追加，長上下文依靠底層 Checkpointer 持久化
    messages: Annotated[List[BaseMessage], add_messages]
    available_skills: List[Dict[str, str]]  # 儲存所有 Skill 的元數據(名稱與描述)
    active_skills: List[str]                # 目前已被「激活」加載進 Context 的 Skill 列表
    mcp_config: Dict[str, Any]              # MCP 伺服器連線組態

# =====================================================================
# 2. Skill 漸進式披露管理器 (Skill Engine)
# =====================================================================
class SkillManager:
    """自動掃描與漸進式讀取 skills/*.md 的管理器"""
    def __init__(self, skills_dir: str = "./skills"):
        self.skills_dir = skills_dir
        if not os.path.exists(skills_dir):
            os.makedirs(skills_dir)

    def scan_available_skills(self) -> List[Dict[str, str]]:
        """第一級：發現。僅讀取 Metadata，消耗極低 Token"""
        skills = []
        for filename in os.listdir(self.skills_dir):
            if filename.endswith(".md"):
                path = os.path.join(self.skills_dir, filename)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # 正則提取 # Skill: Name 與 ## Description
                    name_match = re.search(r"# Skill:\s*(.*)", content)
                    desc_match = re.search(r"## 1\.\s*核心定位\s*\(Intent\)\s*\n(.*)", content)

                    name = name_match.group(1).strip() if name_match else filename
                    desc = desc_match.group(1).strip() if desc_match else "無描述"
                    skills.append({"file": filename, "name": name, "description": desc})
        return skills

    def load_full_skill_content(self, filename: str) -> str:
        """第二級：激活。當使用者意圖命中時，才完整載入 Markdown"""
        path = os.path.join(self.skills_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

# =====================================================================
# 3. LangGraph 節點拓撲實作 (Nodes)
# =====================================================================

# 初始化大腦模型 (使用支援超長 200K Context Window 的 Claude 3.5 Sonnet)
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
skill_mgr = SkillManager()

def load_context_node(state: ClientAgentState):
    """節點一：初始環境與元數據掃描"""
    skills = skill_mgr.scan_available_skills()
    return {"available_skills": skills}

def agent_brain_node(state: ClientAgentState):
    """節點二：核心意圖審審與工具動態綁定"""
    messages = state["messages"]
    available_skills = state["available_skills"]
    active_skills = state.get("active_skills", [])

    # 🧬 策略：動態組裝 System Prompt
    system_base = "你是一個工業級量子計算硬體優化代理人客戶端。\n"

    # 注入可用技能清單 (第一級披露)
    system_base += "=== 當前系統可用技能清單 ===\n"
    for s in available_skills:
        system_base += f"- 技能名稱: {s['name']}, 檔案: {s['file']}\n  意圖定位: {s['description']}\n"

    # 檢查使用者的最後一句話，是否命中某個技能
    # 在生產環境中，這裡可以讓 LLM 先做一次 Route 判斷，此處展示核心邏輯：
    last_user_message = [m.content for m in messages if isinstance(m, HumanMessage)][-1]

    # 動態加載命中技能的完整內容（第二級披露：漸進式揭露）
    loaded_skills_context = ""
    for s in available_skills:
        if s["name"] in last_user_message or "量子" in last_user_message: # 簡易命中策略
            if s["file"] not in active_skills:
                active_skills.append(s["file"])
            full_content = skill_mgr.load_full_skill_content(s["file"])
            loaded_skills_context += f"\n=== 激活並加載技能指南: {s['name']} ===\n{full_content}\n"

    system_prompt = system_base + loaded_skills_context

    # 🔌 核心：動態發現與綁定 MCP Tools (符合 Model Context Protocol)
    # 連線至本地或遠端 MCP 伺服器，動態取得可用工具
    mcp_config = state["mcp_config"]
    with mcp_server_tools_stub(
        command=mcp_config["command"],
        args=mcp_config["args"]
    ) as mcp_tools:

        # 將 MCP 工具與當前動態生成的 System Prompt 綁定至大腦
        llm_with_tools = llm.bind_tools(mcp_tools)

        # 執行大腦推理
        all_messages = [SystemMessage(content=system_prompt)] + messages
        response = llm_with_tools.invoke(all_messages)

        return {"messages": [response], "active_skills": active_skills}

def action_node(state: ClientAgentState):
    """節點三：MCP 實際執行節點"""
    messages = state["messages"]
    last_msg = messages[-1]
    mcp_config = state["mcp_config"]

    # 建立一個工具對照字典
    with mcp_server_tools_stub(command=mcp_config["command"], args=mcp_config["args"]) as mcp_tools:
        tool_map = {t.name: t for t in mcp_tools}

        tool_outputs = []
        for tool_call in last_msg.tool_calls:
            tool_obj = tool_map[tool_call["name"]]
            # 透過 MCP 協議，調用外部實體伺服器（如 PostgreSQL）執行任務
            output = tool_obj.invoke(tool_call["args"])
            tool_outputs.append(output)

        return {"messages": tool_outputs}

# =====================================================================
# 4. 構建狀態圖拓撲與條件路由 (Graph Orchestration)
# =====================================================================

def should_continue_router(state: ClientAgentState) -> Literal["continue", "end"]:
    """判斷大腦是否需要繼續呼叫 MCP 工具，還是直接回答使用者"""
    messages = state["messages"]
    last_msg = messages[-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "continue"
    return "end"

workflow = StateGraph(ClientAgentState)

workflow.add_node("LoadContext", load_context_node)
workflow.add_node("AgentBrain", agent_brain_node)
workflow.add_node("Action", action_node)

workflow.set_entry_point("LoadContext")
workflow.add_edge("LoadContext", "AgentBrain")

# 條件邊：根據 LLM 是否生成 tool_calls 決定走向
workflow.add_conditional_edges(
    "AgentBrain",
    should_continue_router,
    {
        "continue": "Action",
        "end": END
    }
)
workflow.add_edge("Action", "AgentBrain") # 執行完工具後，回到大腦進行反思

# 🚀 關鍵：加入 Memory Checkpointer，確保超長對話上下文能進行語義狀態持久化
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# =====================================================================
# 5. 終端機客戶端測試 Entry
# =====================================================================
if __name__ == "__main__":
    # 配置你們先前實作的 PostgreSQL MCP 伺服器
    mcp_server_config = {
        "command": "docker",
        "args": [
            "run", "-i", "--rm",
            "-e", "DATABASE_URI=postgresql://postgres:your_secure_password@127.0.0.1:5432/quantum_db",
            "crystaldba/postgres-mcp"
        ]
    }

    # 啟動對話執行緒
    config = {"configurable": {"thread_id": "quantum_line_session_001"}}

    print("🚀 自建 LangGraph MCP & Skill 智慧客戶端已就緒。")
    print("輸入 'exit' 退出。")

    while True:
        user_input = input("\n👨‍💻 研發工程師: ")
        if user_input.lower() == 'exit':
            break

        # 傳入初始狀態
        events = app.stream(
            {
                "messages": [HumanMessage(content=user_input)],
                "mcp_config": mcp_server_config
            },
            config,
            stream_mode="values"
        )

        for event in events:
            if "messages" in event and event["messages"]:
                last_msg = event["messages"][-1]
                if isinstance(last_msg, AIMessage) and last_msg.content:
                    print(f"\n🤖 Agent 決策反饋:\n{last_msg.content}")
