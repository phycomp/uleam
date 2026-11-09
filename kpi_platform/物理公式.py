"""KPI 平台：物理推導公式。"""

import math


def 阻抗公式(width_mil, thickness_mil, h_mil, er, material, temp):
    """微帶線阻抗（含超導修正）公式說明。"""
    # Wheeler/Hammerstad 幾何阻抗
    w_h = width_mil / h_mil
    if w_h <= 1:
        eeff = (er + 1) / 2 + ((er - 1) / 2) * (
            (1 + 12 / w_h) ** (-0.5) + 0.04 * (1 - w_h) ** 2
        )
        zo_geo = (60 / math.sqrt(eeff)) * math.log(8 / w_h + 0.25 * w_h)
    else:
        eeff = (er + 1) / 2 + ((er - 1) / 2) * (1 + 12 / w_h) ** (-0.5)
        zo_geo = (120 * math.pi) / (
            math.sqrt(eeff) * (w_h + 1.393 + 0.667 * math.log(w_h + 1.444))
        )
    return {"zo_geo": zo_geo, "eeff": eeff, "w_h": w_h}


def 熱負載公式(area_m2, length_m, t_high, t_low, a, b):
    """傅立葉熱傳導積分：Q = (A/L) * a/(b+1) * (T_high^(b+1) - T_low^(b+1))。"""
    return (area_m2 / length_m) * (a / (b + 1)) * (t_high ** (b + 1) - t_low ** (b + 1))


def 串擾公式(freq_ghz, coupling_length_mm, spacing_um, k):
    """串擾耦合：NEXT/FEXT = 20*log10(k * L/100 * 35/s * factor)。"""
    coupling = k * (coupling_length_mm / 100.0) * (35.0 / spacing_um)
    return 20 * math.log10(max(coupling, 1e-6))


def london_penetration(material, temp):
    """London penetration depth: lambda = lambda_0 / sqrt(1 - (T/Tc)^4)。"""
    tc_map = {"NbTi": 9.2, "Al": 1.2, "Nb": 9.2}
    lambda_0_map = {"NbTi": 240.0, "Al": 50.0, "Nb": 40.0}
    tc = tc_map.get(material, 9.2)
    lambda_0 = lambda_0_map.get(material, 240.0)
    if temp >= tc:
        return 0.0
    return lambda_0 / math.sqrt(1 - (temp / tc) ** 4)
