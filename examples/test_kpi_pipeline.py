"""KPI 平台 pipeline 測試。"""

import sys

sys.path.insert(0, "/home/sam/代理人")
from kpi_platform.KPI驗收 import 驗收全部
from kpi_platform.KPI追蹤 import KPITracker
from kpi_platform.驗證 import 產生測試數據


def test_驗收全部():
    results = 驗收全部()
    assert len(results) == 3
    for r in results:
        assert "kpi" in r and "pass" in r


def test_產生測試數據():
    data = 產生測試數據()
    assert "impedance" in data and "thermal" in data and "crosstalk" in data


def test_KPI追蹤():
    t = KPITracker("/tmp/opencode/kpi_test.json")
    t.add("KPI-1", "阻抗", "50Ω", pass_fail=True)
    s = t.summary()
    assert s["total"] >= 1 and s["passed"] >= 1


if __name__ == "__main__":
    test_驗收全部()
    print("PASS: 驗收全部")
    test_產生測試數據()
    print("PASS: 產生測試數據")
    test_KPI追蹤()
    print("PASS: KPI追蹤")
    print("All KPI pipeline tests passed.")
