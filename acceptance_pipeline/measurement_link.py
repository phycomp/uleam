"""KPI-5 量測單位鏈結：單位換算與台灣量測單位清單。"""

from typing import Any, Dict, List

# 台灣常見量測單位與換算 (to base SI)
_UNITS = {
    "W": 1.0,
    "mW": 1e-3,
    "uW": 1e-6,
    "nW": 1e-9,
    "K": 1.0,
    "mK": 1e-3,
    "m": 1.0,
    "mm": 1e-3,
    "um": 1e-6,
    "Hz": 1.0,
    "GHz": 1e9,
    "MHz": 1e6,
    "dB": 1.0,
}

# 台灣量測單位盤點 (名稱, 類型, 說明)
_TW_UNITS = [
    {"name": "微瓦 (μW)", "type": "power", "note": "低溫熱負載常用"},
    {"name": "毫瓦 (mW)", "type": "power", "note": "室溫段"},
    {"name": "分貝 (dB)", "type": "ratio", "note": "串擾/損耗"},
    {"name": "歐姆 (Ω)", "type": "impedance", "note": "阻抗"},
    {"name": "開爾文 (K)", "type": "temperature", "note": "低溫"},
    {"name": "赫茲 (Hz/GHz)", "type": "frequency", "note": "射頻"},
]


class MeasurementUnitLink:
    def list_units(self) -> List[Dict[str, Any]]:
        return list(_TW_UNITS)

    def get_unit(self, name: str) -> Dict[str, Any]:
        for u in _TW_UNITS:
            if name in u["name"]:
                return dict(u)
        return {}

    def cross_check(self, value: float, from_unit: str, to_unit: str) -> float:
        # 換算：value * (from_factor / to_factor)
        fu = _UNITS.get(from_unit, 1.0)
        tu = _UNITS.get(to_unit, 1.0)
        return value * fu / tu

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        return self.cross_check(value, from_unit, to_unit)


__all__ = ["MeasurementUnitLink"]
