"""KPI 規格載入器：從 YAML/JSON 載入 KPI 指標定義。"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


@dataclass
class KPIStep:
    step_id: str
    requirement: str
    module: str
    status: str = "pending"


@dataclass
class KPISpec:
    kpi_id: str
    title: str
    steps: List[KPIStep] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kpi_id": self.kpi_id,
            "title": self.title,
            "steps": [asdict(s) for s in self.steps],
        }


class KPISpecLoader:
    def __init__(self, path: Optional[str] = None):
        self.path = path
        self._specs: List[KPISpec] = []
        if path:
            self.load(path)

    def load(self, path: str) -> List[KPISpec]:
        with open(path, "r", encoding="utf-8") as f:
            if path.endswith((".yaml", ".yml")):
                if yaml is None:
                    raise RuntimeError("PyYAML not installed")
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
        specs = []
        for k in data.get("kpis", []):
            steps = [KPIStep(**s) for s in k.get("steps", [])]
            specs.append(KPISpec(kpi_id=k["kpi_id"], title=k["title"], steps=steps))
        self._specs = specs
        return specs

    def all(self) -> List[KPISpec]:
        return self._specs

    def by_id(self, kpi_id: str) -> Optional[KPISpec]:
        for s in self._specs:
            if s.kpi_id == kpi_id:
                return s
        return None

    def summary(self) -> Dict[str, Any]:
        total = sum(len(s.steps) for s in self._specs)
        done = sum(1 for s in self._specs for st in s.steps if st.status == "done")
        return {
            "kpi_count": len(self._specs),
            "step_count": total,
            "done": done,
            "pending": total - done,
        }


def load_kpi_spec(path: str) -> List[KPISpec]:
    return KPISpecLoader(path).all()


def default_spec_path() -> str:
    return os.path.join(os.path.dirname(__file__), "kpi_spec.yaml")


# English-friendly aliases
KpiSpec = KPISpec
KpiStep = KPIStep
KpiSpecLoader = KPISpecLoader


__all__ = [
    "KPISpec",
    "KPIStep",
    "KPISpecLoader",
    "load_kpi_spec",
    "default_spec_path",
    "KpiSpec",
    "KpiStep",
    "KpiSpecLoader",
]
