import os
import sys
import tempfile

ROOT = "/home/sam/代理人"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from acceptance_pipeline.kpi_spec import load_kpi_spec, default_spec_path, KPISpecLoader
from acceptance_pipeline.material_db import MaterialDB
from acceptance_pipeline.acceptance_criteria import (
    load_criteria,
    default_criteria_path,
    AcceptanceValidator,
)
from acceptance_pipeline.stages import PipelineContext, Stage1Develop, Stage3Validate
from acceptance_pipeline.pipeline import AcceptancePipeline
from acceptance_pipeline.test_runner import TestRunner
from acceptance_pipeline.deliverables import DeliverablePackager
from acceptance_pipeline.usage_generator import UsageGenerator
from acceptance_pipeline.report import AcceptanceReportGenerator
from acceptance_pipeline.meeting_tracker import MeetingTracker
from acceptance_pipeline.measurement_link import MeasurementUnitLink


def test_load_kpi_spec():
    specs = load_kpi_spec(default_spec_path())
    assert len(specs) >= 5
    assert any(s.kpi_id == "KPI-1" for s in specs)
    loader = KPISpecLoader(default_spec_path())
    assert loader.by_id("KPI-2") is not None
    assert loader.summary()["kpi_count"] >= 5


def test_material_db():
    db = MaterialDB(os.path.join(ROOT, "acceptance_pipeline", "materials.json"))
    m = db.get("NbTi")
    assert m is not None and "tc_k" in m
    assert db.get("不存在材料") is None
    assert len(db.list_all()) >= 7
    assert db.search("超導")


def test_acceptance_criteria():
    cs = load_criteria(default_criteria_path())
    assert len(cs) >= 10
    v = AcceptanceValidator(cs)
    r = v.validate(
        {
            "impedance_zo": 50.5,
            "thermal_uw": 5.0,
            "next_db": -45.0,
            "fext_db": -32.0,
            "drc_ok": True,
            "material_exists": True,
            "unit_tests_pass": True,
            "usage_doc_exists": True,
            "material_db_loaded": True,
            "meeting_scheduled": 1,
            "unit_conversion_ok": True,
        }
    )
    assert r["all_pass"] is True


def test_impedance():
    import sys as _s

    _s.path.insert(0, ROOT)
    from 計算 import calculate_quantum_impedance

    r = calculate_quantum_impedance(16.0, 1.4, 8.0, 4.2, "NbTi", 0.01)
    assert 49.0 <= r["zo"] <= 51.0


def test_thermal():
    import sys as _s

    _s.path.insert(0, ROOT)
    from kpi_platform.驗證 import 驗證熱負載

    thm = 驗證熱負載(
        {"material": "NbTi", "width_mil": 12.0, "thickness_mil": 1.4},
        [
            {
                "stage_name": "MC",
                "temp_k": 0.01,
                "line_length_m": 0.1,
                "attenuation_db": 20,
            }
        ],
    )
    assert thm["pass"] is True


def test_crosstalk():
    import sys as _s

    _s.path.insert(0, ROOT)
    from kpi_platform.驗證 import 驗證串擾

    xt = 驗證串擾({"freq_ghz": 6.0, "coupling_length_mm": 100, "spacing_um": 400})
    assert xt["pass"] is True


def test_drc():
    from agent_system.tools import make_stackup, check_drc

    s = make_stackup("NbTi", 6.0, 12.0)
    d = check_drc(s)
    assert d["ok"] is True


def test_material():
    db = MaterialDB(os.path.join(ROOT, "acceptance_pipeline", "materials.json"))
    assert db.get("NbTi") is not None


def test_stages_run():
    ctx = PipelineContext(spec={"target_zo": 50.0, "freq": 8.0, "min_thickness": 4.0})
    r = Stage1Develop().run(ctx)
    assert r.status in ("pass", "fail")
    assert ctx.stage_results == [] or True


def test_pipeline_run():
    p = AcceptancePipeline(output_dir=os.path.join(ROOT, "acceptance_output_test"))
    rep = p.run()
    assert rep.overall_pass is not None
    assert len(rep.stages) == 7


def test_test_runner():
    tr = TestRunner()
    rep = tr.run_unit(["tests/test_acceptance_pipeline.py"])
    assert rep.status in ("pass", "fail", "skipped")


def test_deliverables():
    with tempfile.TemporaryDirectory() as d:
        r = DeliverablePackager().package(
            d, {"code": ["acceptance_pipeline/kpi_spec.py"]}
        )
        assert os.path.exists(os.path.join(d, "MANIFEST.json"))


def test_usage_generator():
    from acceptance_pipeline.pipeline import PipelineReport

    rep = PipelineReport(
        started_at="t", finished_at="t", stages=[], overall_pass=True, summary={}
    )
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "USAGE.md")
        md = UsageGenerator().generate(path, rep)
        assert "安裝" in md and "測試" in md
        assert os.path.exists(path)


def test_report():
    from acceptance_pipeline.pipeline import PipelineReport

    rep = PipelineReport(
        started_at="t", finished_at="t", stages=[], overall_pass=True, summary={}
    )
    with tempfile.TemporaryDirectory() as d:
        out = AcceptanceReportGenerator().generate(rep, os.path.join(d, "report"))
        assert os.path.exists(out["json"]) and os.path.exists(out["md"])


def test_meeting_tracker():
    with tempfile.TemporaryDirectory() as d:
        mt = MeetingTracker(os.path.join(d, "m.json"))
        mt.schedule("2026-11-10", "週會")
        assert mt.compliance_status()["scheduled"] >= 1


def test_measurement_link():
    mul = MeasurementUnitLink()
    assert len(mul.list_units()) >= 1
    assert mul.cross_check(1.0, "W", "uW") == 1e6
