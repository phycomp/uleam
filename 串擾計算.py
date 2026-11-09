"""串擾計算模組：NEXT/FEXT/串擾損耗模型。"""

import math


def next_db(freq_ghz: float, coupling_length_mm: float, spacing_um: float) -> float:
    """近端串擾 NEXT (dB)：簡化模型。"""
    if spacing_um <= 0:
        return 0.0
    k = 0.1  # 耦合係數
    coupling = k * (coupling_length_mm / 100.0) * (35.0 / spacing_um)
    return 20 * math.log10(max(coupling, 1e-6))


def fext_db(freq_ghz: float, coupling_length_mm: float, spacing_um: float) -> float:
    """遠端串擾 FEXT (dB)。"""
    if spacing_um <= 0:
        return 0.0
    k = 0.05
    coupling = (
        k * (coupling_length_mm / 100.0) * (35.0 / spacing_um) * math.sqrt(freq_ghz)
    )
    return 20 * math.log10(max(coupling, 1e-6))


def crosstalk_loss_db(next_val: float, fext_val: float) -> float:
    """總串擾損耗 (dB)。"""
    return 10 * math.log10(10 ** (next_val / 10) + 10 ** (fext_val / 10))


def evaluate_crosstalk(spec: dict) -> dict:
    """依規格評估串擾。"""
    freq = spec.get("freq_ghz", 6.0)
    length = spec.get("coupling_length_mm", 100.0)
    spacing = spec.get("spacing_um", 100.0)
    n = next_db(freq, length, spacing)
    f = fext_db(freq, length, spacing)
    return {
        "next_db": round(n, 2),
        "fext_db": round(f, 2),
        "total_crosstalk_db": round(crosstalk_loss_db(n, f), 2),
    }
