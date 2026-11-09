"""驗收標準定義 + 驗證器。"""

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


@dataclass
class AcceptanceCriterion:
    criterion_id: str
    kpi_id: str
    stage: int
    metric: str
    operator: str
    threshold: Any
    test_ref: Optional[str] = None


def load_criteria(path: str) -> List[AcceptanceCriterion]:
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith((".yaml", ".yml")):
            data = yaml.safe_load(f)
        else:
            data = json.load(f)
    out = []
    for c in data.get("criteria", []):
        out.append(AcceptanceCriterion(**c))
    return out


def default_criteria_path() -> str:
    return os.path.join(os.path.dirname(__file__), "acceptance_criteria.yaml")


class AcceptanceValidator:
    def __init__(self, criteria: List[AcceptanceCriterion]):
        self.criteria = criteria

    def _check(self, c: AcceptanceCriterion, value: Any) -> bool:
        op = c.operator
        thr = c.threshold
        if op == "<=":
            return value <= thr
        if op == ">=":
            return value >= thr
        if op == "==":
            return value == thr
        if op == "!=":
            return value != thr
        if op == "in_range":
            lo, hi = thr
            return lo <= value <= hi
        if op == "contains":
            return thr in value
        return False

    def validate(self, results: Dict[str, Any]) -> Dict[str, Any]:
        checks = []
        for c in self.criteria:
            val = results.get(c.metric, None)
            # missing metric -> fail (unless not provided)
            if val is None and c.metric not in results:
                ok = False
            else:
                try:
                    ok = self._check(c, val)
                except Exception:
                    ok = False
            checks.append(
                {
                    "criterion_id": c.criterion_id,
                    "kpi_id": c.kpi_id,
                    "metric": c.metric,
                    "value": val,
                    "pass": ok,
                }
            )
        all_pass = all(ch["pass"] for ch in checks) if checks else True
        return {
            "all_pass": all_pass,
            "checks": checks,
            "passed": sum(1 for ch in checks if ch["pass"]),
            "total": len(checks),
        }

    def by_stage(self, stage: int) -> List[AcceptanceCriterion]:
        return [c for c in self.criteria if c.stage == stage]

    def by_kpi(self, kpi_id: str) -> List[AcceptanceCriterion]:
        return [c for c in self.criteria if c.kpi_id == kpi_id]


def merge_with_kpi_platform(
    criteria: List[AcceptanceCriterion], platform_items: List[Dict[str, Any]]
) -> List[AcceptanceCriterion]:
    """合併 YAML criteria 與 KPI 平台 JSON 項目，去重 (by criterion_id / item)."""
    seen = {c.criterion_id for c in criteria}
    out = list(criteria)
    for it in platform_items or []:
        cid = it.get("kpi_id", "") + ":" + it.get("item", "")
        if cid in seen:
            continue
        seen.add(cid)
        # 平台項目轉為 criteria（寬鬆）
        out.append(
            AcceptanceCriterion(
                criterion_id=cid or "PLATFORM",
                kpi_id=it.get("kpi_id", ""),
                stage=0,
                metric="platform_item",
                operator="==",
                threshold=it.get("pass_fail"),
                test_ref=None,
            )
        )
    return out


__all__ = [
    "AcceptanceCriterion",
    "AcceptanceValidator",
    "load_criteria",
    "default_criteria_path",
    "merge_with_kpi_platform",
]
