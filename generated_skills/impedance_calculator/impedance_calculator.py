"""Impedance Calculator Skill：封裝 calculate_quantum_impedance。"""
import sys
sys.path.insert(0, "/home/sam/代理人")
from 計算 import calculate_quantum_impedance


class ImpedanceCalculator:
    def __init__(self, er: float = 4.2, temp: float = 0.01):
        # TODO: AI 推論部分 - 參數驗證與單位轉換
        self.er = er
        self.temp = temp

    def compute(self, width_mil, thickness_mil, h_mil, material="Cu"):
        # TODO: AI 推論部分 - 材料/溫度邊界檢查
        return calculate_quantum_impedance(
            width_mil=width_mil,
            thickness_mil=thickness_mil,
            h_mil=h_mil,
            er=self.er,
            material=material,
            temp=self.temp,
        )