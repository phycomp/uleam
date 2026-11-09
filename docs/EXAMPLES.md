# Examples — 代理人專案

## 1. 阻抗計算
```bash
cd /home/sam/代理人
/home/sam/flex/bin/python -c "
import sys; sys.path.insert(0,'.')
from 計算 import calculate_quantum_impedance
r = calculate_quantum_impedance(12.0, 1.4, 8.0, 4.2, 'NbTi', 0.01)
print('Zo:', r['zo'], 'SC:', r['is_superconducting'])
"
```

## 2. 熱負載計算
```bash
cd /home/sam/代理人
/home/sam/flex/bin/python -c "
import sys; sys.path.insert(0,'.')
from 計算 import calculate_coupled_thermal_load
stackup = {'material': 'Cu', 'width_mil': 12.0, 'thickness_mil': 1.4}
stages = [{'stage_name': 'MC', 'temp_k': 0.01, 'line_length_m': 0.1, 'attenuation_db': 20}]
print(calculate_coupled_thermal_load(stackup, stages))
"
```

## 3. 串擾計算
```bash
cd /home/sam/代理人
/home/sam/flex/bin/python -c "
import sys; sys.path.insert(0,'.')
from 串擾計算 import evaluate_crosstalk
print(evaluate_crosstalk({'freq_ghz': 6.0, 'coupling_length_mm': 100, 'spacing_um': 100}))
"
```

## 4. 三視圖生成
```bash
cd /home/sam/代理人
/home/sam/flex/bin/python -c "
import sys; sys.path.insert(0,'.')
from 三視圖 import 繪製全部視圖
spec = {'name':'CF3','channels':8,'pitch_mm':2.0,'line_width_um':35,'dielectric_thickness_mm':0.129,'signal_thickness_um':35,'total_width_mm':16.0,'length_mm':100.0}
f1,f2,f3 = 繪製全部視圖(spec, font_size=12, zoom=1.5)
print('views:', f1 is not None, f2 is not None, f3 is not None)
"
```

## 5. KPI Pipeline 測試
```bash
cd /home/sam/代理人
/home/sam/flex/bin/python examples/test_kpi_pipeline.py
```

## 6. 材質驗收
```bash
cd /home/sam/代理人
/home/sam/flex/bin/python -c "
import sys; sys.path.insert(0,'.')
from 材質數據庫 import 驗收材質
print(驗收材質('NbTi', {'tc_k': 9.0, 'density_g_cm3': 6.1}))
"
```

## 7. Streamlit UI
```bash
cd /home/sam/代理人
streamlit run app.py
```