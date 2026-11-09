# KPI 規格平台 — 完整 Pipeline

## Pipeline 流程

```
KPI規格指標 → 開發量子傳輸線 → 測試 → 驗證 → 交付 → 使用說明+測試+材料數據庫 → 各階段驗收KPI
```

### 階段 1：KPI 規格指標
- 定義 KPI-1..KPI-5（雲端平台、會議、電性 SOP、熱負載 SOP、量測單位）。
- 文件：`docs/KPI_COMPLIANCE.md`、`合約書/量子柔性連接線計畫書.md`。

### 階段 2：開發量子傳輸線
- 核心模組：`計算.py`、`疊構Util.py`、`代理主程式.py`、`元件整合.py`、`串擾計算.py`、`LLM解析.py`、`三視圖.py`、`材質數據庫.py`。
- 技能：`generic-qcable`、`quantum-cryogenic-cable`、`crosstalk-calc`、`electrical-spec`、`thermal-load-*`、`component-integration`、`connector`、`three-view`、`material-db`、`llm-parser`。

### 階段 3：測試
- Smoke tests：`examples/test_example.py`
- 單一技能測試：`generated_skills/<skill>/test_*.py`
- 編譯檢查：`py_compile`
- 測試文件：`docs/TEST_GUIDE.md`

### 階段 4：驗證
- `kpi_platform/驗證.py`：驗證阻抗/熱負載/串擾。
- `kpi_platform/KPI驗收.py`：各階段 KPI 驗收（KPI-1/KPI-3/KPI-4）。
- 測試數據：`產生測試數據()`。

### 階段 5：交付
- KPI 交付文件：`kpi_platform/KPI追蹤.py`（KPITracker），欄位：日期、KPI編號、KPI項目、驗證標準、通過否、備註（可擴充）。
- 交付項目：程式碼、測試程式、驗證程式+測試數據、KPI交付文件、說明文件。

### 階段 6：使用說明 + 測試 + 材質數據庫
- 使用說明：`docs/USAGE.md`、`docs/KPI_PLATFORM.md`。
- 測試：`docs/TEST_GUIDE.md`、`examples/test_example.py`。
- 材質數據庫：`材質數據庫.py`、`material-db` 技能。

### 階段 7：各階段驗收 KPI
- 執行 `kpi_platform/KPI驗收.py` → `驗收全部()` 回傳各 KPI 驗收結果。

## 補充（原 pipeline 缺口已補齊）
- LLM 解析模組（KPI-1-8）：`LLM解析.py` + `llm-parser` 技能。
- 量測單位鏈結（KPI-5）：`measurement-unit-link` 技能。
- 熱負載溫區擴充（KPI-4：300K/150K/40K）：`thermal-load-measurement` 已更新。
- 電性 SOP + 串擾（KPI-3）：`electrical-spec`、`electrical-test-sop`、`crosstalk-calc`。
- 雲端佈署（KPI-1-1）：`cloud-deploy` 技能 + Docker/wrangler 設定。

## 使用範例
```python
import sys; sys.path.insert(0, "/home/sam/代理人")
from kpi_platform.KPI驗收 import 驗收全部
from kpi_platform.KPI追蹤 import KPITracker
results = 驗收全部()
for r in results:
    print(r["kpi"], r["pass"])
tracker = KPITracker("kpi_data.json")
for r in results:
    tracker.add(r["kpi"], r["kpi"], str(r), pass_fail=r["pass"])
print(tracker.summary())
```