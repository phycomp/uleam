import sys
import os

sys.path.insert(0, "/home/sam/代理人")

import streamlit as st

st.set_page_config(page_title="驗收 Pipeline", layout="wide")
st.title("✅ 量子傳輸線驗收 Pipeline")

with st.sidebar:
    st.subheader("執行選項")
    run_all = st.button("執行完整 Pipeline")
    stage_sel = st.multiselect("指定階段", [0, 1, 2, 3, 4, 5, 6], default=[])

if run_all or stage_sel:
    with st.spinner("執行中..."):
        from acceptance_pipeline.pipeline import AcceptancePipeline

        stages = stage_sel if stage_sel else None
        rep = AcceptancePipeline().run(stages=stages)
    st.success(f"整體：{'PASS' if rep.overall_pass else 'FAIL'}")
    st.metric(
        "通過階段",
        f"{rep.summary.get('passed', 0)}/{rep.summary.get('stage_count', 0)}",
    )
    for s in rep.stages:
        with st.expander(f"Stage {s.stage_id} {s.name} — {s.status}"):
            st.write("KPI checks:", s.kpi_checks)
            if s.errors:
                st.error(s.errors)
    # report
    from acceptance_pipeline.report import AcceptanceReportGenerator
    import tempfile

    outdir = "/home/sam/代理人/acceptance_output"
    os.makedirs(outdir, exist_ok=True)
    paths = AcceptanceReportGenerator().generate(rep, os.path.join(outdir, "report"))
    st.write("報告：", paths)
else:
    st.info("點擊「執行完整 Pipeline」開始。")
    # material db preview
    st.subheader("材料數據庫")
    try:
        from acceptance_pipeline.material_db import MaterialDB

        db = MaterialDB()
        st.write(db.to_list())
    except Exception as e:
        st.warning(str(e))
    st.subheader("KPI 規格")
    try:
        from acceptance_pipeline.kpi_spec import load_kpi_spec, default_spec_path

        specs = load_kpi_spec(default_spec_path())
        st.write([s.to_dict() for s in specs])
    except Exception as e:
        st.warning(str(e))
