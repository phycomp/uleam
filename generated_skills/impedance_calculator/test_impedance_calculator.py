import sys, importlib.util
sys.path.insert(0, "/home/sam/代理人")
spec = importlib.util.spec_from_file_location("ic", "/home/sam/代理人/generated_skills/impedance_calculator/impedance_calculator.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
IC = m.ImpedanceCalculator

def test_compute_cu():
    r = IC().compute(12.0, 1.4, 8.0, "Cu")
    assert "zo" in r and r["zo"] > 0

def test_compute_sc():
    r = IC().compute(12.0, 1.4, 8.0, "NbTi")
    assert r["is_superconducting"] is True