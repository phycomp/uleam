"""KPI 平台：KPI 追蹤（日期/KPI項目/驗證標準/通過否）。"""

import json
import os
from datetime import datetime


class KPITracker:
    def __init__(self, path="kpi_data.json"):
        self.path = path
        self.items = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)

    def add(self, kpi_id, item, standard, pass_fail=None, date=None, notes=""):
        entry = {
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "kpi_id": kpi_id,
            "item": item,
            "standard": standard,
            "pass_fail": pass_fail,
            "notes": notes,
        }
        self.items.append(entry)
        self._save()
        return entry

    def update(self, idx, **kwargs):
        if 0 <= idx < len(self.items):
            self.items[idx].update(kwargs)
            self._save()

    def list_all(self):
        return self.items

    def summary(self):
        total = len(self.items)
        passed = sum(1 for x in self.items if x.get("pass_fail") is True)
        failed = sum(1 for x in self.items if x.get("pass_fail") is False)
        pending = total - passed - failed
        return {"total": total, "passed": passed, "failed": failed, "pending": pending}
