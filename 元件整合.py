"""元件整合模組：衰減器 / LPF / Infrared Filter 模型（仿 CF3 整合至 FPC/Uleam1）。"""

import math
import numpy as np


def attenuator_dissipation(input_power_dbm: float, attenuation_db: float) -> float:
    """衰減器自發熱 (W)：P_in*(1-10^(-α/10))，P_in 以 W。"""
    p_in_w = 10 ** ((input_power_dbm - 30) / 10)
    return p_in_w * (1 - 10 ** (-attenuation_db / 10))


def lpf_cutoff(fc_hz: float, r_ohm: float, c_farad: float) -> float:
    """一階 LPF 截止頻率 fc = 1/(2πRC)。回傳計算值以驗證。"""
    return 1.0 / (2 * math.pi * r_ohm * c_farad)


def lpf_attenuation(freq_hz: float, fc_hz: float) -> float:
    """一階 LPF 在 freq 的衰減 (dB)。"""
    if fc_hz <= 0:
        return 0.0
    ratio = freq_hz / fc_hz
    return -10 * math.log10(1 + ratio**2)


def infrared_filter_transmission(
    wavelength_um: float, cutoff_um: float, slope: float = 10.0
) -> float:
    """IR filter 傳輸 (0-1)：sigmoid 型截止。"""
    return 1.0 / (1.0 + math.exp(slope * (wavelength_um - cutoff_um)))


def integrate_components(spec: dict) -> dict:
    """將衰減器/LPF/IR filter 整合至規格，回傳元件參數摘要。"""
    att_db = spec.get("attenuation_db", 20.0)
    fc = spec.get("lpf_cutoff_hz", 1e9)
    ir_cutoff = spec.get("ir_cutoff_um", 5.0)
    return {
        "attenuator_db": att_db,
        "attenuator_heat_w_at_-30dbm": attenuator_dissipation(-30.0, att_db),
        "lpf_cutoff_hz": fc,
        "lpf_at_6ghz_db": lpf_attenuation(6e9, fc),
        "ir_cutoff_um": ir_cutoff,
        "ir_transmission_at_10um": infrared_filter_transmission(10.0, ir_cutoff),
    }
