import sys, importlib.util
sys.path.insert(0, "/home/sam/代理人")
spec = importlib.util.spec_from_file_location("csr", "/home/sam/代理人/generated_skills/cross_section_renderer/cross_section_renderer.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
CSR = m.CrossSectionRenderer

def test_parse():
    ast = {"stackup": [
        {"layer_name": "D1", "type": "dielectric", "thickness": 10, "color": "#fff", "conductors": []},
        {"layer_name": "C1", "type": "conductor_layer", "thickness": 2, "color": "#f00", "conductors": [], "etch_factor": 90},
    ]}
    reg, di, co, vi = CSR().parse(ast)
    assert isinstance(reg, dict)
    assert len(di) + len(co) >= 1