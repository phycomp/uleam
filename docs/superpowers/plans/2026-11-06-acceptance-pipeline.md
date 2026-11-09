# Acceptance Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立完整量子傳輸線驗收 pipeline：KPI 規格指標 → 開發 → 測試 → 驗證 → 交付 → 使用說明+測試+材料數據庫，各階段 KPI 驗收，產出程式碼、使用+測試文件、驗收標準、交付項目；補齊材料數據庫、驗收標準定義、交付打包、使用說明產生器、KPI-2 會議追蹤、KPI-5 量測單位整合、CI 腳本等缺口。

**Architecture:** 新增 `acceptance_pipeline/` 套件，以 YAML 規格檔定義 KPI 與驗收標準，Python 模組提供載入、驗證、執行、打包、報告能力；Streamlit 頁面整合；pytest 三層測試（單元/整合/驗收）；材料數據庫以 JSON + Python API 持久化。

**Tech Stack:** Python 3.11+, PyYAML (或 json fallback), pytest, streamlit, 現有 計算.py / 串擾計算.py / kpi_platform / agent_system

**Spec:** docs/KPI_COMPLIANCE.md, docs/KPI_PLATFORM.md, docs/FEATURES.md

## Global Constraints

- Python 3.11+ (現有環境)
- 路徑使用 `/home/sam/代理人` 為根，sys.path.insert(0, root)
- 中文命名允許（現有程式碼慣例），但公開 API 必須提供英文別名
- KPI 閾值：阻抗 50Ω ±1Ω；熱負載 ≤ 10 μW；NEXT ≤ -40 dB；FEXT ≤ -30 dB；最小介質厚度 4 mil
- 材料：Cu, NbTi, Nb, Al, Rogers RO4003C, PTFE, High-Res Silicon
- 測試框架：pytest
- 交付物：程式碼 + 使用說明 + 測試文件 + 驗收標準 + 交付項目 + 材料數據庫
- 不修改現有模組行為，僅新增 wrapper/整合

## Review Focus

- 材料數據庫查詢在材料不存在時應回傳結構化錯誤而非拋例外
- 驗收標準 YAML 與 KPI 平台 JSON 兩種來源合併時不得重複或遺漏
- pipeline 部分階段失敗時應記錄失敗並繼續，不得中斷整個流程
- 測試執行器在 pytest 未安裝時應優雅降級並回報
- Streamlit 頁面不得在 import 時觸發計算（延遲到按鈕）

## File Structure

```
acceptance_pipeline/
  __init__.py
  kpi_spec.py          # KPI 指標定義 + YAML/JSON 載入
  kpi_spec.yaml         # KPI 規格資料
  material_db.py        # 材料數據庫 API
  materials.json        # 材料數據
  acceptance_criteria.py # 驗收標準定義 + 驗證器
  acceptance_criteria.yaml # 驗收標準資料
  stages.py             # 7 個階段 runner
  pipeline.py           # 編排器
  test_runner.py        # pytest 編排
  deliverables.py       # 交付打包
  usage_generator.py    # 使用說明產生器
  report.py             # 驗收報告產生器
  meeting_tracker.py    # KPI-2 會議追蹤
  measurement_link.py   # KPI-5 量測單位整合
pages/
  11驗收Pipeline.py     # Streamlit UI
tests/
  test_acceptance_pipeline.py
docs/
  ACCEPTANCE_PIPELINE.md # 使用說明
scripts/
  run_acceptance.sh     # CI 腳本
```

---

### Task 1: 套件骨架 + KPI 規格載入器

**Files:**
- Create: `acceptance_pipeline/__init__.py`
- Create: `acceptance_pipeline/kpi_spec.py`
- Create: `acceptance_pipeline/kpi_spec.yaml`

**Interfaces:**
- Produces: `KPISpec` dataclass (kpi_id, title, steps: list of {step_id, requirement, module, status}), `load_kpi_spec(path) -> list[KPISpec]`, `KPISpecLoader.load_all() -> dict`

- [ ] **Step 1: Write failing test**

```python
# tests/test_acceptance_pipeline.py (partial)
def test_load_kpi_spec():
    from acceptance_pipeline.kpi_spec import load_kpi_spec
    specs = load_kpi_spec("acceptance_pipeline/kpi_spec.yaml")
    assert len(specs) >= 5
    assert any(s.kpi_id == "KPI-1" for s in specs)
```

- [ ] **Step 2: Run test to verify fail** — `pytest tests/test_acceptance_pipeline.py::test_load_kpi_spec -v` Expected: ModuleNotFoundError

- [ ] **Step 3: Implement** `acceptance_pipeline/kpi_spec.py`：定義 `KPISpec` dataclass、`load_kpi_spec(path)`，支援 YAML 與 JSON fallback；`KPISpecLoader` 類別封裝載入與 by_id 查詢。kpi_spec.yaml 包含 KPI-1..KPI-5 完整步驟（從 docs/KPI_COMPLIANCE.md 轉錄）。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit** — `git add acceptance_pipeline/ tests/test_acceptance_pipeline.py && git commit -m "feat: add kpi spec loader"`

---

### Task 2: 材料數據庫

**Files:**
- Create: `acceptance_pipeline/material_db.py`
- Create: `acceptance_pipeline/materials.json`

**Interfaces:**
- Consumes: none
- Produces: `MaterialDB` class with `get(name) -> dict | None`, `list_all() -> list[str]`, `search(keyword) -> list[dict]`, `add(material)`, `to_dataframe()`；模組層級 `get_material(name)` 便利用函式

- [ ] **Step 1: Write failing test**

```python
def test_material_db():
    from acceptance_pipeline.material_db import MaterialDB
    db = MaterialDB("acceptance_pipeline/materials.json")
    m = db.get("NbTi")
    assert m is not None and "tc_k" in m
    assert db.get("不存在材料") is None  # 結構化錯誤，不拋例外
    assert len(db.list_all()) >= 7
```

- [ ] **Step 2: Run test to verify fail**

- [ ] **Step 3: Implement** `materials.json` 含 7 種材料完整屬性（導電率、熱導率係數 a/b、介電常數、損耗角、Tc、lambda0、最小厚度、供應商、備註）；`material_db.py` 實作 `MaterialDB` 與 `get_material`。材料不存在時回傳 None 並記錄 warning，不拋例外。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit**

---

### Task 3: 驗收標準定義

**Files:**
- Create: `acceptance_pipeline/acceptance_criteria.py`
- Create: `acceptance_pipeline/acceptance_criteria.yaml`

**Interfaces:**
- Produces: `AcceptanceCriterion` (criterion_id, kpi_id, stage, metric, threshold, operator, test_ref), `AcceptanceValidator.validate(results) -> dict`, `load_criteria(path)`, `merge_with_kpi_platform(criteria, platform_items) -> list`

- [ ] **Step 1: Write failing test**

```python
def test_acceptance_criteria():
    from acceptance_pipeline.acceptance_criteria import load_criteria, AcceptanceValidator
    cs = load_criteria("acceptance_pipeline/acceptance_criteria.yaml")
    assert len(cs) >= 10
    v = AcceptanceValidator(cs)
    r = v.validate({"impedance_zo": 50.5, "thermal_uw": 5.0, "next_db": -45.0, "fext_db": -32.0})
    assert r["all_pass"] is True
```

- [ ] **Step 2: Run test to verify fail**

- [ ] **Step 3: Implement** criteria YAML 定義每個 KPI 每階段的指標/閾值/運算子/測試參考；validator 支援 >=, <=, ==, in_range；merge_with_kpi_platform 去重合併。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit**

---

### Task 4: 七階段 runner

**Files:**
- Create: `acceptance_pipeline/stages.py`

**Interfaces:**
- Produces: `StageRunner` base with `run(ctx) -> StageResult`；`Stage0KpiSpec`, `Stage1Develop`, `Stage2Test`, `Stage3Validate`, `Stage4Deliver`, `Stage5DocsDb`, `Stage6Accept`；`StageResult` dataclass (stage_id, name, status, kpi_checks, artifacts, errors)

- [ ] **Step 1: Write failing test**

```python
def test_stages_run():
    from acceptance_pipeline.stages import PipelineContext, Stage1Develop
    ctx = PipelineContext(spec={"target_zo": 50.0, "freq": 8.0, "min_thickness": 4.0})
    r = Stage1Develop().run(ctx)
    assert r.status in ("pass", "fail")
    assert "solution_pool" in r.artifacts or r.errors
```

- [ ] **Step 2: Run test to verify fail**

- [ ] **Step 3: Implement** stages.py：每個 stage 獨立可測，失敗記錄 errors 並繼續；Stage1 呼叫 agent_system 或 deterministic fallback（無 LLM 時用 tools）；Stage2 呼叫 test_runner；Stage3 呼叫 kpi_platform 驗證；Stage4 打包；Stage5 產生 docs+DB；Stage6 KPI 驗收。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit**

---

### Task 5: 編排器

**Files:**
- Create: `acceptance_pipeline/pipeline.py`

**Interfaces:**
- Produces: `AcceptancePipeline.run(ctx=None, stages=None) -> PipelineReport`；`PipelineReport` (started_at, finished_at, stages: list[StageResult], overall_pass, summary)；支援 `--stage` 選擇性執行

- [ ] **Step 1: Write failing test**

```python
def test_pipeline_run():
    from acceptance_pipeline.pipeline import AcceptancePipeline
    p = AcceptancePipeline()
    rep = p.run()
    assert rep.overall_pass is not None
    assert len(rep.stages) == 7
```

- [ ] **Step 2: Run test to verify fail**

- [ ] **Step 3: Implement** pipeline.py 編排 7 階段，任一失敗不中斷，彙總 report，寫入 `acceptance_report.json`。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit**

---

### Task 6: 測試執行器

**Files:**
- Create: `acceptance_pipeline/test_runner.py`

**Interfaces:**
- Produces: `TestRunner.run_unit(paths)`, `run_integration()`, `run_acceptance()`, `run_all() -> TestReport`；pytest 不存在時回傳 status="skipped"

- [ ] **Step 1: Write failing test**

```python
def test_test_runner():
    from acceptance_pipeline.test_runner import TestRunner
    tr = TestRunner()
    rep = tr.run_unit(["tests/test_acceptance_pipeline.py"])
    assert rep.status in ("pass", "fail", "skipped")
```

- [ ] **Step 2: Run test to verify fail**

- [ ] **Step 3: Implement** test_runner.py 用 subprocess 呼叫 pytest，解析 exit code；無 pytest 時 skipped。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit**

---

### Task 7: 交付打包器

**Files:**
- Create: `acceptance_pipeline/deliverables.py`

**Interfaces:**
- Produces: `DeliverablePackager.package(output_dir, artifacts) -> dict`；打包 code/docs/tests/db/report 到 output_dir，產生 MANIFEST.json

- [ ] **Step 1: Write failing test**

```python
def test_deliverables():
    import tempfile, os
    from acceptance_pipeline.deliverables import DeliverablePackager
    with tempfile.TemporaryDirectory() as d:
        r = DeliverablePackager().package(d, {"code": ["acceptance_pipeline/kpi_spec.py"]})
        assert os.path.exists(os.path.join(d, "MANIFEST.json"))
```

- [ ] **Step 2: Run test to verify fail**

- [ ] **Step 3: Implement** deliverables.py：複製檔案、產生 MANIFEST.json（含 checksum、timestamp）、zip 打包可選。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit**

---

### Task 8: 使用說明產生器

**Files:**
- Create: `acceptance_pipeline/usage_generator.py`

**Interfaces:**
- Produces: `UsageGenerator.generate(output_path, pipeline_report) -> str`；自動產生 markdown 使用說明，含安裝、執行、測試、KPI 驗收章節

- [ ] **Step 1: Write failing test**

```python
def test_usage_generator():
    from acceptance_pipeline.usage_generator import UsageGenerator
    from acceptance_pipeline.pipeline import PipelineReport
    rep = PipelineReport(started_at="t", finished_at="t", stages=[], overall_pass=True, summary={})
    md = UsageGenerator().generate("/tmp/USAGE.md", rep)
    assert "安裝" in md and "測試" in md
```

- [ ] **Step 2: Run test to verify fail**

- [ ] **Step 3: Implement** usage_generator.py：模板化 markdown 產生，嵌入 pipeline report 摘要與 KPI 結果。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit**

---

### Task 9: 驗收報告產生器

**Files:**
- Create: `acceptance_pipeline/report.py`

**Interfaces:**
- Produces: `AcceptanceReportGenerator.generate(report, output_path) -> dict`；JSON + Markdown 雙輸出

- [ ] **Step 1: Write failing test**

```python
def test_report():
    import tempfile, os
    from acceptance_pipeline.report import AcceptanceReportGenerator
    from acceptance_pipeline.pipeline import PipelineReport
    rep = PipelineReport(started_at="t", finished_at="t", stages=[], overall_pass=True, summary={})
    with tempfile.TemporaryDirectory() as d:
        out = AcceptanceReportGenerator().generate(rep, os.path.join(d, "report"))
        assert os.path.exists(out["json"]) and os.path.exists(out["md"])
```

- [ ] **Step 2: Run test to verify fail**

- [ ] **Step 3: Implement** report.py：JSON dump + markdown 摘要。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit**

---

### Task 10: KPI-2 會議追蹤器

**Files:**
- Create: `acceptance_pipeline/meeting_tracker.py`

**Interfaces:**
- Produces: `MeetingTracker` with `schedule`, `record_minutes`, `list_meetings`, `compliance_status`；JSON 持久化

- [ ] **Step 1: Write failing test**

```python
def test_meeting_tracker():
    import tempfile
    from acceptance_pipeline.meeting_tracker import MeetingTracker
    with tempfile.TemporaryDirectory() as d:
        mt = MeetingTracker(os.path.join(d, "m.json"))
        mt.schedule("2026-11-10", "週會")
        assert mt.compliance_status()["scheduled"] >= 1
```

- [ ] **Step 2: Run test to verify fail**

- [ ] **Step 3: Implement** meeting_tracker.py。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit**

---

### Task 11: KPI-5 量測單位整合

**Files:**
- Create: `acceptance_pipeline/measurement_link.py`

**Interfaces:**
- Produces: `MeasurementUnitLink` 包裝 measurement-unit-link skill 資料：`list_units()`, `get_unit(name)`, `cross_check(value, from_unit, to_unit)`

- [ ] **Step 1: Write failing test**

```python
def test_measurement_link():
    from acceptance_pipeline.measurement_link import MeasurementUnitLink
    mul = MeasurementUnitLink()
    assert len(mul.list_units()) >= 1
```

- [ ] **Step 2: Run test to verify fail**

- [ ] **Step 3: Implement** measurement_link.py：內建台灣量測單位清單（μW/W/mK/dB 轉換），cross_check 做單位換算。

- [ ] **Step 4: Run test** — Expected: PASS

- [ ] **Step 5: Commit**

---

### Task 12: Streamlit 頁面

**Files:**
- Create: `pages/11驗收Pipeline.py`

**Interfaces:**
- Streamlit UI：側邊欄選擇階段/執行；主區顯示 KPI、測試結果、報告；按鈕觸發（不 import 時計算）

- [ ] **Step 1: Write page** with lazy imports and button-triggered runs.

- [ ] **Step 2: Smoke test** — `python -c "import ast; ast.parse(open('pages/11驗收Pipeline.py').read())"` Expected: no syntax error

- [ ] **Step 3: Commit**

---

### Task 13: CI 腳本

**Files:**
- Create: `scripts/run_acceptance.sh`

**Interfaces:**
- bash 腳本：設定 PYTHONPATH、執行 pytest、執行 pipeline、輸出報告

- [ ] **Step 1: Write script**

- [ ] **Step 2: chmod +x and smoke test** — `bash scripts/run_acceptance.sh --dry-run`

- [ ] **Step 3: Commit**

---

### Task 14: 使用說明文件

**Files:**
- Create: `docs/ACCEPTANCE_PIPELINE.md`

**Interfaces:**
- Markdown 使用說明：安裝、執行、測試、KPI 驗收、交付物

- [ ] **Step 1: Write doc**

- [ ] **Step 2: Commit**

---

### Task 15: 完整 pytest 測試套件

**Files:**
- Modify: `tests/test_acceptance_pipeline.py`（擴充所有模組測試）

**Interfaces:**
- 覆蓋 Task 1-11 的所有公開 API

- [ ] **Step 1: Add comprehensive tests**

- [ ] **Step 2: Run full suite** — `pytest tests/test_acceptance_pipeline.py -v` Expected: all PASS

- [ ] **Step 3: Commit**

---

### Task 16: 自我審查與缺口補充驗證

- [ ] **Step 1: 跑完整 pipeline** — `python -c "from acceptance_pipeline.pipeline import AcceptancePipeline; print(AcceptancePipeline().run().overall_pass)"`
- [ ] **Step 2: 修補執行時發現的缺口**
- [ ] **Step 3: Final commit**

## Self-Review Checklist

- [ ] Spec coverage: KPI-1..5 全部有 task
- [ ] Type consistency: 所有介面簽名一致
- [ ] Review Focus: 5 項全有測試
- [ ] Proportion: plan 長度合理
