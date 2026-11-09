"""測試範例：彙總所有技能的 smoke tests。"""
import sys, importlib.util
sys.path.insert(0, "/home/sam/代理人")

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def test_impedance():
    m = load("ic", "/home/sam/代理人/generated_skills/impedance_calculator/impedance_calculator.py")
    r = m.ImpedanceCalculator().compute(12.0, 1.4, 8.0, "Cu")
    assert r["zo"] > 0

def test_thermal():
    m = load("tl", "/home/sam/代理人/generated_skills/thermal_load/thermal_load.py")
    r = m.ThermalLoadCalculator().compute({"material": "Cu", "width_mil": 12.0, "thickness_mil": 1.4})
    assert r["total_load_w"] >= 0

def test_cross_section():
    m = load("csr", "/home/sam/代理人/generated_skills/cross_section_renderer/cross_section_renderer.py")
    ast = {"stackup": [{"layer_name": "D1", "type": "dielectric", "thickness": 10, "color": "#fff", "conductors": []}]}
    reg, *_ = m.CrossSectionRenderer().parse(ast)
    assert isinstance(reg, dict)

def test_greeter():
    m = load("gr", "/home/sam/代理人/generated_skills/greeter/greeter.py")
    assert m.Greeter().greet("X") == "Hello, X!"

def test_notifier():
    m = load("nf", "/home/sam/代理人/generated_skills/notifier/notifier.py")
    assert m.Notifier(["sms"]).send("hi", "0912") is True

def test_dsl_parser():
    import pandas as pd
    m = load("dp", "/home/sam/代理人/generated_skills/dsl_parser/dsl_parser.py")
    df = pd.DataFrame([{"名稱": "L1", "厚度um": 10, "材料": "FR4", "DK": 4.2, "DF": 0.02,
                        "顏色": "#fff", "邊緣": "#000", "是訊號層": False}])
    ast = m.DSLParserSkill().csv_to_ast(df)
    assert "stackup" in ast

def test_agent_workflow():
    m = load("aw", "/home/sam/代理人/generated_skills/agent_workflow/agent_workflow.py")
    state = {"target_zo": 50.0, "frequency_ghz": 6.0, "temperature_profile": [],
             "current_stackup": [], "is_symmetric": True, "electrical_results": {},
             "thermal_results": {}, "coherence_score": 0.0, "iteration_count": 0,
             "solution_pool": []}
    r = m.AgentWorkflowSkill(max_iter=1).run(state)
    assert r["iteration_count"] >= 1

if __name__ == "__main__":
    for name in ["test_impedance", "test_thermal", "test_cross_section", "test_greeter",
                 "test_notifier", "test_dsl_parser", "test_agent_workflow"]:
        globals()[name]()
        print(f"PASS: {name}")
    print("All example tests passed.")