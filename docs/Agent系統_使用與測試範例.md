# LangGraph + CrewAI + Llama3 代理人系統 — 使用與測試範例

## 0. 環境
- Python venv: `/home/sam/代理人/.venv` (Python 3.14)
- 啟用：`source /home/sam/代理人/.venv/bin/activate`
- Ollama：`ollama serve` (port 11434)，模型 `llama3:8b`
- 驗證：`ollama list` / `curl http://localhost:11434/api/tags`

## 1. 模組匯入測試
```bash
cd /home/sam/代理人
source .venv/bin/activate
python -c "import agent_system.config, agent_system.state, agent_system.tools, agent_system.crew, agent_system.llm, agent_system.nodes, agent_system.graph; print('IMPORT OK')"
```

## 2. 工具層單元測試（確定性，無 LLM）
```python
from agent_system.tools import calc_impedance_and_loss, calc_thermal_load, check_drc, check_guardrail, make_stackup

# 阻抗
r = calc_impedance_and_loss(10.0, 20.0, "Rogers RO4003C", 8.0)
assert "Zo" in r and "alpha_d" in r
print("Zo:", r["Zo"], "Ω")

# 堆疊
s = make_stackup("Cu", 10.0, 20.0)
print(s)

# DRC
d = check_drc(s)
print("DRC:", d)

# Guardrail
elec = calc_impedance_and_loss(10.0, 5.5, "NbTi", 8.0)
therm = calc_thermal_load(s)
gr = check_guardrail(elec, therm, check_drc(s))
print("Guardrail:", gr)
```
執行：`python -c "..."` 或存成 `tests/test_tools.py`。

## 3. LLM 連線測試 (Ollama)
```bash
# 直接測試
curl -s http://localhost:11434/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"llama3:8b","messages":[{"role":"user","content":"Reply OK"}],"max_tokens":8}'

# Python
python -c "from agent_system.llm import chat; print(chat('You are a tester.','Say OK only.'))"
```

## 4. CrewAI 角色測試
```python
from agent_system.crew import researcher_agent, reporter_agent
from crewai import Task, Crew
a = researcher_agent()
t = Task(description="Summarize Dk of Rogers RO4003C in one sentence.", expected_output="One sentence.", agent=a)
print(Crew(agents=[a], tasks=[t], verbose=False).kickoff())
```

## 5. LangGraph 完整流程測試
```python
import os
os.environ["MAX_ITERATIONS"] = "6"
os.environ["SOLUTION_POOL_TARGET"] = "2"
from agent_system.graph import run
r = run({"target_zo": 50.0, "freq": 8.0, "min_thickness": 4.0}, thread_id="demo")
print("status:", r.get("status"))
print("iters:", r.get("iteration_count"))
print("pool:", len(r.get("solution_pool", [])))
for s in r.get("solution_pool", []):
    print("  Zo=", s["elec"]["Zo"], s["stackup"][1]["material"],
          "W=", round(s["stackup"][1]["width_mil"], 2),
          "H=", round(s["stackup"][0]["thickness_mil"], 2))
print("trace:", [t["node"] for t in r.get("trace_log", [])])
```
執行：`python test_run.py`（見下方）。

## 6. Streamlit UI 測試
```bash
cd /home/sam/代理人
source .venv/bin/activate
streamlit run app.py
# 瀏覽器開啟 http://localhost:8501
# 側邊欄調整 Spec → 點 "Run Optimization" → 查看 Agent Trace 頁面
```

## 7. SQLite Checkpoint 測試（恢復）
```python
import sqlite3
conn = sqlite3.connect("/home/sam/代理人/agent_checkpoints.sqlite")
print(conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
```

## 8. 測試腳本（tests/test_agent.py）
建立 `/home/sam/代理人/tests/test_agent.py`：
```python
import os
os.environ.setdefault("MAX_ITERATIONS", "4")
os.environ.setdefault("SOLUTION_POOL_TARGET", "2")

def test_tools():
    from agent_system.tools import calc_impedance_and_loss, make_stackup, check_drc
    r = calc_impedance_and_loss(10.0, 5.5, "NbTi", 8.0)
    assert 40 <= r["Zo"] <= 60, r
    s = make_stackup("NbTi", 10.0, 5.5)
    d = check_drc(s)
    assert d["ok"], d
    print("test_tools PASS")

def test_llm():
    from agent_system.llm import chat
    out = chat("Reply only OK.", "ping")
    assert isinstance(out, str)
    print("test_llm PASS:", out[:40])

def test_graph():
    from agent_system.graph import run
    r = run({"target_zo": 50.0, "freq": 8.0, "min_thickness": 4.0}, thread_id="t")
    assert r.get("status") == "done"
    assert len(r.get("solution_pool", [])) >= 1
    print("test_graph PASS: pool=", len(r["solution_pool"]))

if __name__ == "__main__":
    test_tools()
    test_llm()
    test_graph()
    print("ALL AGENT TESTS PASS")
```
執行：`python tests/test_agent.py`

## 9. 常見問題
- **Ollama 未啟動**：`ollama serve` 或 `systemctl status ollama`
- **模型缺失**：`ollama pull llama3:8b`
- **VRAM 不足**：改用 `OLLAMA_MODEL=llama3:8b` (Q4 預設)；避免 70B
- **SQLite 鎖定**：刪除 `agent_checkpoints.sqlite` 重建
- **Streamlit port 佔用**：`streamlit run app.py --server.port 8502`