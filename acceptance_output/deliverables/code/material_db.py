"""材料數據庫：JSON 持久化 + Python 查詢 API。"""

import json
import os
import warnings
from typing import Any, Dict, List, Optional


class MaterialDB:
    def __init__(self, path: Optional[str] = None):
        if path is None:
            path = os.path.join(os.path.dirname(__file__), "materials.json")
        self.path = path
        self._data: Dict[str, Any] = {"materials": []}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {"materials": []}

    def _save(self):
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def _items(self) -> List[Dict[str, Any]]:
        return self._data.get("materials", [])

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        for m in self._items():
            if m.get("name") == name:
                return dict(m)
        warnings.warn(f"material not found: {name}")
        return None

    def list_all(self) -> List[str]:
        return [m.get("name") for m in self._items()]

    def search(self, keyword: str) -> List[Dict[str, Any]]:
        kw = keyword.lower()
        out = []
        for m in self._items():
            hay = " ".join(str(v) for v in m.values()).lower()
            if kw in hay:
                out.append(dict(m))
        return out

    def add(self, material: Dict[str, Any]) -> bool:
        if not material.get("name"):
            return False
        if self.get(material["name"]) is not None:
            return False
        self._data.setdefault("materials", []).append(material)
        self._save()
        return True

    def to_list(self) -> List[Dict[str, Any]]:
        return [dict(m) for m in self._items()]

    # pandas-friendly alias
    def to_dataframe(self):
        try:
            import pandas as pd

            return pd.DataFrame(self.to_list())
        except Exception:  # pragma: no cover
            return self.to_list()


def get_material(name: str, path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    return MaterialDB(path).get(name)


__all__ = ["MaterialDB", "get_material"]
