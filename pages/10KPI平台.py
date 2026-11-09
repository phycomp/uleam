from streamlit import (
    columns,
    dataframe,
    markdown,
    number_input,
    selectbox,
    set_page_config,
    sidebar,
    subheader,
    success,
    title,
    write,
)
import streamlit as st
import sys

sys.path.insert(0, "/home/sam/代理人")
from kpi_platform.KPI追蹤 import KPITracker
from kpi_platform.驗證 import 產生測試數據

set_page_config(page_title="KPI 規格平台", layout="wide")
title("📋 KPI 規格平台 — 量子傳輸線")

tracker = KPITracker("/home/sam/代理人/kpi_data.json")

# 側邊欄：新增 KPI
with sidebar:
    subheader("新增 KPI 項目")
    kpi_id = st.text_input("KPI 編號", "KPI-1")
    item = st.text_input("KPI 項目", "")
    standard = st.text_input("驗證標準", "")
    status = st.selectbox("通過否", ["未驗證", "通過", "未通過"])
    notes = st.text_input("備註", "")
    if st.button("新增"):
        pf = None if status == "未驗證" else (status == "通過")
        tracker.add(kpi_id, item, standard, pass_fail=pf, notes=notes)
        success("已新增")

# 主區：列表
subheader("KPI 清單")
items = tracker.list_all()
if items:
    dataframe(items, use_container_width=True)
else:
    write("尚無 KPI 項目。")

# 測試數據
subheader("驗證測試數據")
if st.button("產生測試數據"):
    data = 產生測試數據()
    write(data)
    for k, v in data.items():
        if isinstance(v, dict) and "pass" in v:
            st.metric(k, "PASS" if v["pass"] else "FAIL")
