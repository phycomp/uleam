import sys, importlib.util
import pandas as pd
sys.path.insert(0, "/home/sam/代理人")
spec = importlib.util.spec_from_file_location("dp", "/home/sam/代理人/generated_skills/dsl_parser/dsl_parser.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
DPS = m.DSLParserSkill

def test_parse():
    ast = {"stackup": [
        {"layer_name": "D1", "type": "dielectric", "thickness": 10, "color": "#fff", "conductors": []},
    ]}
    reg, di, co, vi = DPS().parse(ast)
    assert isinstance(reg, dict)

def test_csv_to_ast():
    df = pd.DataFrame([{
        "名稱": "L1", "厚度um": 10, "材料": "FR4", "DK": 4.2, "DF": 0.02,
        "顏色": "#fff", "邊緣": "#000", "是訊號層": False
    }])
    ast = DPS().csv_to_ast(df)
    assert ast is not None and "stackup" in ast