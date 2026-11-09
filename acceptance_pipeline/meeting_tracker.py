"""KPI-2 每週定期會議追蹤器。"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


class MeetingTracker:
    def __init__(self, path: str = "meetings.json"):
        self.path = path
        self._items: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save(self):
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._items, f, ensure_ascii=False, indent=2)

    def schedule(
        self, date: str, title: str, attendees: List[str] = None
    ) -> Dict[str, Any]:
        entry = {
            "date": date,
            "title": title,
            "attendees": attendees or [],
            "minutes": "",
            "created_at": datetime.now().isoformat(),
        }
        self._items.append(entry)
        self._save()
        return entry

    def record_minutes(self, idx: int, minutes: str) -> bool:
        if 0 <= idx < len(self._items):
            self._items[idx]["minutes"] = minutes
            self._save()
            return True
        return False

    def list_meetings(self) -> List[Dict[str, Any]]:
        return list(self._items)

    def compliance_status(self) -> Dict[str, Any]:
        return {
            "scheduled": len(self._items),
            "with_minutes": sum(1 for m in self._items if m.get("minutes")),
            "pass": len(self._items) >= 1,
        }


__all__ = ["MeetingTracker"]
