"""Streamlit page: Agent-First optimization with trace visualization."""
import streamlit as st
import json

st.set_page_config(layout="wide")
st.title("🤖 Agent-First 量子傳輸線優化 (LangGraph + CrewAI + Llama3)")

# sidebar spec
with st.sidebar:
    st.header("Spec")
    target_zo = st.slider("目標 Zo (Ω)", 40.0, 60.0, 50.0, 0.5)
    freq = st.slider("頻率 (GHz)", 4.0, 12.0, 8.0, 0.5)
    min_thick = st.slider("最小介質厚度 (mil)", 2.0, 10.0, 4.0, 0.5)
    thread_id = st.text_input("Thread ID", value="run1")
    run_btn = st.button("🚀 Run Optimization")

col_trace, col_result = st.columns([2, 1])

if run_btn:
    import os
    os.environ.setdefault("TARGET_ZO", str(target_zo))
    os.environ.setdefault("MIN_THICKNESS_MIL", str(min_thick))
    # reload config not needed; pass via spec
    from agent_system.graph import run
    spec = {"target_zo": target_zo, "freq": freq, "min_thickness": min_thick}
    with st.spinner("Agents running..."):
        try:
            result = run(spec, thread_id=thread_id)
        except Exception as e:
            st.error(f"Run failed: {e}")
            result = None
    if result:
        st.session_state["last_result"] = result

result = st.session_state.get("last_result")
if result:
    with col_result:
        st.subheader("結果")
        st.write("Status:", result.get("status"))
        st.write("Iterations:", result.get("iteration_count"))
        st.write("Solution pool:", len(result.get("solution_pool", [])))
        for i, s in enumerate(result.get("solution_pool", [])):
            st.markdown(f"**Solution {i+1}**")
            st.json(s.get("elec"))
            st.write("thermal:", s.get("thermal"))
            st.code(str(s.get("stackup")))
        if result.get("messages"):
            st.subheader("Reporter")
            for m in result["messages"]:
                st.write(m.get("content"))
    with col_trace:
        st.subheader("Agent Trace")
        for entry in result.get("trace_log", []):
            with st.expander(f"{entry['node']}  @ {round(entry['ts'],1)}"):
                st.write("decision:", entry.get("decision"))
                st.json({"input": entry.get("input"), "output": entry.get("output")})
else:
    with col_trace:
        st.info("按下 Run 開始優化。")