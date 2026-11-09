import sys, importlib.util
sys.path.insert(0, "/home/sam/代理人")
spec = importlib.util.spec_from_file_location("tl", "/home/sam/代理人/generated_skills/thermal_load/thermal_load.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
TLC = m.ThermalLoadCalculator

def test_compute():
    stackup = {"material": "Cu", "width_mil": 12.0, "thickness_mil": 1.4}
    r = TLC().compute(stackup)
    assert "total_load_w" in r and r["total_load_w"] >= 0