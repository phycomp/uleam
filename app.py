"""統一入口：整合 pages/ 下的 Streamlit 頁面 (重構整合產物)"""

import streamlit as st

pages = [
    st.Page("pages/01主程式II.py", title="量子傳輸線 AI Agent 模擬器 V2", icon="🎛️"),
    st.Page("pages/02DSL描述.py", title="DSL 描述與截面", icon="📐"),
    st.Page("pages/03擴充自動化.py", title="多導體傳輸線自動化分析", icon="🚀"),
    st.Page("pages/04全功能匯出探石.py", title="N通道總線 S 參數分析", icon="📊"),
    st.Page("pages/05通用型截面.py", title="通用型截面 DSL 渲染器", icon="🧩"),
    st.Page("pages/06DSL產生器II.py", title="PyAnsys 腳本產生器", icon="🔧"),
    st.Page("pages/07雙軌實作II.py", title="PCB 11 層堆疊渲染器", icon="🧱"),
    st.Page("pages/07語法2多邊2截面.py", title="DSL 向量多邊形截面", icon="🔷"),
    st.Page("pages/08csv2截面.py", title="FPC 疊構 CSV→截面", icon="📄"),
    st.Page("pages/09阻抗計算.py", title="阻抗計算 (4-12GHz)", icon="⚡"),
    st.Page(
        "pages/10AgentTrace.py", title="Agent-First 優化 (LangGraph+CrewAI)", icon="🤖"
    ),
    st.Page("pages/10KPI平台.py", title="KPI 規格平台", icon="📋"),
]

pg = st.navigation(pages)
pg.run()
