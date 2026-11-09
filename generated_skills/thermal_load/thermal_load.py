"""Thermal Load Skill：封裝 calculate_coupled_thermal_load。"""
import sys
sys.path.insert(0, "/home/sam/代理人")
from 計算 import calculate_coupled_thermal_load


class ThermalLoadCalculator:
    def __init__(self, stages=None):
        # TODO: AI 推論部分 - 預設溫度分層與驗證
        self.stages = stages or [
            {"stage_name": "Room Temp", "temp_k": 300.0, "line_length_m": 0.5, "attenuation_db": 0},
            {"stage_name": "MC Stage", "temp_k": 0.01, "line_length_m": 0.1, "attenuation_db": 20},
        ]

    def compute(self, stackup):
        # TODO: AI 推論部分 - stackup 結構驗證
        return calculate_coupled_thermal_load(stackup, self.stages)