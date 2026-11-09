"""執行範例：示範如何使用 generated_skills 下的技能。"""
import sys, importlib.util
sys.path.insert(0, "/home/sam/代理人")

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

# 1. Impedance Calculator
ic = load("ic", "/home/sam/代理人/generated_skills/impedance_calculator/impedance_calculator.py")
calc = ic.ImpedanceCalculator(er=4.2, temp=0.01)
print("Impedance:", calc.compute(12.0, 1.4, 8.0, "NbTi"))

# 2. Thermal Load
tl = load("tl", "/home/sam/代理人/generated_skills/thermal_load/thermal_load.py")
stackup = {"material": "Cu", "width_mil": 12.0, "thickness_mil": 1.4}
print("Thermal:", tl.ThermalLoadCalculator().compute(stackup))

# 3. Cross-Section Renderer
csr = load("csr", "/home/sam/代理人/generated_skills/cross_section_renderer/cross_section_renderer.py")
ast = {"stackup": [
    {"layer_name": "D1", "type": "dielectric", "thickness": 10, "color": "#fff", "conductors": []},
    {"layer_name": "C1", "type": "conductor_layer", "thickness": 2, "color": "#f00", "conductors": [], "etch_factor": 90},
]}
reg, di, co, vi = csr.CrossSectionRenderer().parse(ast)
print("Cross-section layers:", len(reg), "dielectrics:", len(di), "conductors:", len(co))

# 4. Greeter
gr = load("gr", "/home/sam/代理人/generated_skills/greeter/greeter.py")
print("Greeter:", gr.Greeter("Hi").greet("Sam"))

# 5. Notifier
nf = load("nf", "/home/sam/代理人/generated_skills/notifier/notifier.py")
print("Notifier:", nf.Notifier(["sms", "email"]).send("hello", "0912"))

# 6. DSL Parser
dp = load("dp", "/home/sam/代理人/generated_skills/dsl_parser/dsl_parser.py")
import pandas as pd
df = pd.DataFrame([{"名稱": "L1", "厚度um": 10, "材料": "FR4", "DK": 4.2, "DF": 0.02,
                    "顏色": "#fff", "邊緣": "#000", "是訊號層": False}])
print("DSL AST keys:", list(dp.DSLParserSkill().csv_to_ast(df).keys()))

# 7. Agent Workflow
aw = load("aw", "/home/sam/代理人/generated_skills/agent_workflow/agent_workflow.py")
state = {"target_zo": 50.0, "frequency_ghz": 6.0, "temperature_profile": [],
         "current_stackup": [], "is_symmetric": True, "electrical_results": {},
         "thermal_results": {}, "coherence_score": 0.0, "iteration_count": 0,
         "solution_pool": []}
res = aw.AgentWorkflowSkill(max_iter=2).run(state)
print("Agent iterations:", res["iteration_count"])