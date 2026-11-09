# KPI 規格平台 (KPI Platform)

## 功能
1. **物理推導公式**：`kpi_platform/物理公式.py`（阻抗、熱負載、串擾、London penetration）。
2. **測試程式**：`kpi_platform/驗證.py`（驗證阻抗/熱負載/串擾）。
3. **驗證程式 + 測試數據**：`產生測試數據()` 產生一組測試數據。
4. **KPI 交付文件**：`kpi_platform/KPI追蹤.py`（KPITracker），欄位：日期、KPI項目、驗證標準、通過否、備註。可擴充。
5. **說明文件**：本文件 + `docs/KPI_COMPLIANCE.md`。
6. **其它功能**：Streamlit UI（`pages/10KPI平台.py`）、JSON 儲存、摘要統計。

## 使用方式
```bash
cd /home/sam/代理人
streamlit run app.py  # 選擇 KPI 規格平台 頁面
```

或程式化：
```python
import sys; sys.path.insert(0, "/home/sam/代理人")
from kpi_platform.KPI追蹤 import KPITracker
from kpi_platform.驗證 import 產生測試數據
t = KPITracker("kpi_data.json")
t.add("KPI-1", "阻抗計算", "50Ω ±1Ω", pass_fail=True)
print(t.summary())
print(產生測試數據())
```

## 擴充欄位
KPITracker.add() 支援任意 kwargs，可擴充欄位（如 responsible、due_date、evidence）。