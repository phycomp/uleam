"""三視圖模組：前/側/上視圖，拆解為獨立函式（字型、縮放）。"""

import math
from matplotlib.pyplot import subplots, tight_layout
from matplotlib.patches import Rectangle


def _尺寸(spec):
    n_ch = spec.get("channels", 8)
    pitch = spec.get("pitch_mm", 2.0)
    w = spec.get("line_width_um", 35) / 1000.0
    h = spec.get("dielectric_thickness_mm", 0.129)
    t = spec.get("signal_thickness_um", 35) / 1000.0
    total_w = spec.get("total_width_mm", n_ch * pitch)
    L = spec.get("length_mm", 100.0)
    total_h = 2 * h + 3 * t
    return n_ch, pitch, w, h, t, total_w, L, total_h


def 設定字型(ax, size=10, family="sans-serif"):
    """獨立函式：設定座標軸字型大小與字體。"""
    if ax is None:
        return
    ax.tick_params(labelsize=size)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(size)
        label.set_fontfamily(family)


def 設定縮放(ax, zoom=1.0):
    """獨立函式：設定視圖縮放（zoom >1 放大）。"""
    if ax is None:
        return
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    cx = (xlim[0] + xlim[1]) / 2
    cy = (ylim[0] + ylim[1]) / 2
    hw = (xlim[1] - xlim[0]) / (2 * zoom)
    hh = (ylim[1] - ylim[0]) / (2 * zoom)
    ax.set_xlim(cx - hw, cx + hw)
    ax.set_ylim(cy - hh, cy + hh)


def 繪製前視圖(spec, ax=None, font_size=10, zoom=1.0):
    """前視圖：層結構截面（X-Y 平面）。"""
    n_ch, pitch, w, h, t, total_w, L, total_h = _尺寸(spec)
    cond = spec.get("conductor_color", "#FFD700")
    diel = spec.get("dielectric_color", "#C4956A")
    if ax is None:
        fig, ax = subplots(figsize=(10, 7))
    else:
        fig = ax.figure
    y0, y1, y2, y3, y4 = 0, t, t + h, t + h + t, t + h + t + h
    ax.add_patch(
        Rectangle((0, y0), total_w, t, facecolor="#8B9CAD", edgecolor="#4A5568")
    )
    ax.add_patch(
        Rectangle((0, y4), total_w, t, facecolor="#8B9CAD", edgecolor="#4A5568")
    )
    ax.add_patch(Rectangle((0, y1), total_w, h, facecolor=diel, edgecolor="#744210"))
    ax.add_patch(Rectangle((0, y3), total_w, h, facecolor=diel, edgecolor="#744210"))
    for i in range(n_ch):
        ax.add_patch(
            Rectangle((i * pitch, y2), w, t, facecolor=cond, edgecolor="#B8860B")
        )
    ax.set_xlim(-0.5, total_w + 0.5)
    ax.set_ylim(-0.1, total_h + 0.1)
    ax.set_title(
        f"前視圖 Front View ({spec.get('name', '')})",
        fontsize=font_size + 1,
        fontweight="bold",
    )
    設定字型(ax, font_size)
    設定縮放(ax, zoom)
    return fig, ax


def 繪製側視圖(spec, ax=None, font_size=10, zoom=1.0):
    """側視圖：沿長度方向的剖面（Z-Y 平面）。"""
    n_ch, pitch, w, h, t, total_w, L, total_h = _尺寸(spec)
    cond = spec.get("conductor_color", "#FFD700")
    diel = spec.get("dielectric_color", "#C4956A")
    if ax is None:
        fig, ax = subplots(figsize=(10, 6))
    else:
        fig = ax.figure
    y0, y1, y2, y3, y4 = 0, t, t + h, t + h + t, t + h + t + h
    ax.add_patch(Rectangle((0, y0), L, t, facecolor="#8B9CAD", edgecolor="#4A5568"))
    ax.add_patch(Rectangle((0, y4), L, t, facecolor="#8B9CAD", edgecolor="#4A5568"))
    ax.add_patch(
        Rectangle((0, y1), L, h, facecolor=diel, edgecolor="#744210", alpha=0.6)
    )
    ax.add_patch(
        Rectangle((0, y3), L, h, facecolor=diel, edgecolor="#744210", alpha=0.6)
    )
    ax.add_patch(Rectangle((0, y2), L, t, facecolor=cond, edgecolor="#B8860B"))
    ax.set_xlim(0, L)
    ax.set_ylim(-0.1, total_h + 0.1)
    ax.set_title(
        f"側視圖 Side View ({spec.get('name', '')})",
        fontsize=font_size + 1,
        fontweight="bold",
    )
    設定字型(ax, font_size)
    設定縮放(ax, zoom)
    return fig, ax


def 繪製上視圖(spec, ax=None, font_size=10, zoom=1.0):
    """上視圖：俯視圖（X-Z 平面）。"""
    n_ch, pitch, w, h, t, total_w, L, total_h = _尺寸(spec)
    cond = spec.get("conductor_color", "#FFD700")
    if ax is None:
        fig, ax = subplots(figsize=(10, 6))
    else:
        fig = ax.figure
    for i in range(n_ch):
        ax.add_patch(
            Rectangle((0, i * pitch), L, w, facecolor=cond, edgecolor="#B8860B")
        )
    ax.set_xlim(0, L)
    ax.set_ylim(0, total_w)
    ax.set_title(
        f"上視圖 Top View ({spec.get('name', '')})",
        fontsize=font_size + 1,
        fontweight="bold",
    )
    ax.set_xlabel("Length (mm)")
    ax.set_ylabel("Width (mm)")
    設定字型(ax, font_size)
    設定縮放(ax, zoom)
    return fig, ax


def 繪製全部視圖(spec, font_size=10, zoom=1.0):
    """一次產生前/側/上三視圖，回傳 (fig_front, fig_side, fig_top)。"""
    f1, _ = 繪製前視圖(spec, font_size=font_size, zoom=zoom)
    f2, _ = 繪製側視圖(spec, font_size=font_size, zoom=zoom)
    f3, _ = 繪製上視圖(spec, font_size=font_size, zoom=zoom)
    return f1, f2, f3
