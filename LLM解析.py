"""LLM 自然語法解析模組：將中文描述轉為傳輸線參數。"""

import re


def 解析參數(描述: str) -> dict:
    """啟發式解析：從中文描述提取通道數、間距、線寬等。"""
    params = {}
    # 通道數
    m = re.search(r"(\d+)\s*通道", 描述)
    if m:
        params["channels"] = int(m.group(1))
    # 間距 mm
    m = re.search(r"間距\s*(\d+\.?\d*)\s*mm", 描述)
    if m:
        params["pitch_mm"] = float(m.group(1))
    # 線寬 um
    m = re.search(r"線寬\s*(\d+)\s*μ?m", 描述)
    if m:
        params["line_width_um"] = int(m.group(1))
    # 材料
    for mat in ["Cu", "NbTi", "Nb", "Ag"]:
        if mat in 描述:
            params["material"] = mat
    # 頻率 GHz
    m = re.search(r"(\d+\.?\d*)\s*GHz", 描述)
    if m:
        params["freq_ghz"] = float(m.group(1))
    return params


def 生成參數(描述: str, spec_name: str = "") -> dict:
    """LLM 輔助參數生成（啟發式 fallback，無 API 時使用）。"""
    params = 解析參數(描述)
    params.setdefault("channels", 8)
    params.setdefault("pitch_mm", 2.0)
    params.setdefault("line_width_um", 35)
    params.setdefault("material", "NbTi")
    params.setdefault("freq_ghz", 6.0)
    params["spec_name"] = spec_name
    return params
