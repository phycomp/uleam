# 使用說明 (Usage)

## 快速開始

### 1. 啟動 Streamlit UI
```bash
cd /home/sam/代理人
streamlit run app.py
```

### 2. 執行範例
```bash
cd /home/sam/代理人
python examples/run_example.py
```

### 3. 執行測試
```bash
cd /home/sam/代理人
python examples/test_example.py
```

## 模組使用

### 計算阻抗
```python
import sys; sys.path.insert(0, "/home/sam/代理人")
from 計算 import calculate_quantum_impedance
r = calculate_quantum_impedance(12.0, 1.4, 8.0, 4.2, "NbTi", 0.01)
print(r["zo"], r["is_superconducting"])
```

### 熱負載
```python
from 計算 import calculate_coupled_thermal_load
stackup = {"material": "Cu", "width_mil": 12.0, "thickness_mil": 1.4}
stages = [{"stage_name": "MC", "temp_k": 0.01, "line_length_m": 0.1, "attenuation_db": 20}]
print(calculate_coupled_thermal_load(stackup, stages))
```

### 截面解析
```python
from 疊構Util import 疊構解析
ast = {"stackup": [{"layer_name": "D1", "type": "dielectric", "thickness": 10, "color": "#fff", "conductors": []}]}
reg, di, co, vi = 疊構解析(ast)
```

### 元件整合
```python
from 元件整合 import integrate_components
print(integrate_components({"attenuation_db": 20, "lpf_cutoff_hz": 1e9, "ir_cutoff_um": 5}))
```

### 代理人狀態機
```python
from 代理主程式 import run_workflow
state = {"target_zo": 50.0, "frequency_ghz": 6.0, "temperature_profile": [],
         "current_stackup": [], "is_symmetric": True, "electrical_results": {},
         "thermal_results": {}, "coherence_score": 0.0, "iteration_count": 0,
         "solution_pool": []}
res = run_workflow(state, max_iter=2)
print(res["iteration_count"])
```

## 技能使用
- OpenCode 技能：在對話中輸入 `/skill-name` 或觸發條件描述。
- 程式化技能：`generated_skills/<skill>/<skill>.py`。

## 文件索引
- `docs/SKILLS_INDEX.md`：技能清單暨使用情境
- `docs/TEST_GUIDE.md`：測試指南
- `docs/USAGE_FLOW.md`：使用流程
- `docs/FEATURES.md`：功能清單
- `REFACTOR_MANIFEST.md`：重構進度