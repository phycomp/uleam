from streamlit import code, columns, markdown, pyplot, set_page_config, subheader
from matplotlib.pyplot import subplots
from yaml import safe_load
from 疊構Util import 疊構解析

# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt
import matplotlib.patches as patches
# import yaml
from fontUtil2 import 配置中文#, 配置字型
配置中文()
# 字=配置字型()

# ==============================================================================
# 0. 網頁基本配置
# ==============================================================================
set_page_config(page_title="PCB 11層堆疊正確向量渲染器", layout="wide")

# ==============================================================================
# 1. 您提供的輸入參數語法樹 (完全對接您的 DSL 內容)
# ==============================================================================
DSL_INPUT = """
stackup:
- layer_name: L1_SOLDER_MASK
  type: 介電
  thickness: 25
  color: '#1b4d3e'
  conductors: []
- layer_name: L2_SIGNAL_TOP
  type: 導電
  thickness: 35
  color: '#ffaa00'
  conductors:
  - mode: absolute
    name: Diff_P
    width: 100.0
    x_center: -150.0
  - mode: absolute
    name: Diff_N
    width: 100.0
    x_center: 0.0
  etch_factor: 90
- layer_name: L3_PREPREG_1
  type: 介電
  thickness: 100
  color: '#aa9f7f'
  conductors: []
- layer_name: L4_PLANE_1
  type: 導電
  thickness: 35
  color: '#cc6600'
  conductors: []
  etch_factor: 90
- layer_name: L5_CORE_1
  type: 介電
  thickness: 150
  color: '#8c8266'
  conductors: []
- layer_name: L6_SIGNAL_MID1
  type: 導電
  thickness: 18
  color: '#ffaa00'
  conductors:
  - mode: repeat
    name: Bus_Ch
    width: 50.0
    x_start: 100.0
    spacing: 80.0
    count: 4
  etch_factor: 90
- layer_name: L7_CORE_2
  type: 介電
  thickness: 150
  color: '#8c8266'
  conductors: []
- layer_name: L8_PLANE_2
  type: 導電
  thickness: 35
  color: '#cc6600'
  conductors: []
  etch_factor: 90
- layer_name: L9_PREPREG_2
  type: 介電
  thickness: 100
  color: '#aa9f7f'
  conductors: []
- layer_name: L10_SIGNAL_BOT
  type: 導電
  thickness: 35
  color: '#ffaa00'
  conductors: []
  etch_factor: 90
- layer_name: L11_SOLDER_BOT
  type: 介電
  thickness: 25
  color: '#1b4d3e'
  conductors: []
vias:
- name: Laser_Via_1
  type: blind
  start_layer: L2_SIGNAL_TOP
  end_layer: L4_PLANE_1
  x_center: -150.0
  drill_diameter: 90.0
  color: '#e64a19'
"""

# ==============================================================================
# 3. 網頁渲染佈局
# ==============================================================================
ast_data = safe_load(DSL_INPUT)
y_registry, dielectrics, conductors, vias = 疊構解析(ast_data)

col_plot, col_dsl = columns([2, 1])

with col_plot:
    subheader("🖼️ 正確的 PCB 向量多邊形截面圖")
    fig, ax = subplots(figsize=(11, 6))
    ax.set_facecolor("#151515") # 使用高級暗色模式底色
    
    # 1. 繪製介電層大背景
    for di in dielectrics:
        ax.add_patch(patches.Polygon(di["poly"], closed=True, facecolor=di["color"], edgecolor="#333333", alpha=0.9, linewidth=0.5))
        # 於右側標記層有名稱
        ax.text(420, (di["poly"][0,1] + di["poly"][2,1])/2, di["name"], color="#888888", va="center", fontsize=8)
        
    # 2. 繪製金屬層 (平面或獨立 Traces) - 嵌入包覆
    for co in conductors:
        ax.add_patch(patches.Polygon(co["poly"], closed=True, facecolor=co["color"], edgecolor="#ffffff", linewidth=0.8, zorder=3))
        
    # 3. 繪製盲孔 (Laser Via) - 斜紋填充金屬柱
    for vi in vias:
        ax.add_patch(patches.Polygon(vi["poly"], closed=True, facecolor=vi["color"], edgecolor="#ffffff", hatch='//', linewidth=1.0, zorder=4))
        ax.text(vi["poly"][0,0]-10, (vi["poly"][0,1]+vi["poly"][2,1])/2, vi["name"], color="#ffffff", ha="right", va="center", fontsize=8, zorder=5)

    # 設置畫布刻度與極限
    ax.set_xlim(-400, 550)
    max_total_height = max([v["top"] for v in y_registry.values()])
    ax.set_ylim(-10, max_total_height + 20)
    ax.set_xlabel("橫向坐標 Width (μm)", fontsize=10)
    ax.set_ylabel("縱向堆疊實體高度 Height (μm)", fontsize=10)  #, fontproperties=字)
    ax.grid(True, color="#2a2a2a", linestyle=":", linewidth=0.5)
    
    pyplot(fig)

with col_dsl:
    subheader("🌲 輸入的原始 DSL 語法樹")
    code(DSL_INPUT, language="yaml")
with sidebar:
  subheader("🛡️ 修正版：符合硬體拓樸的 PCB 11層截面向量渲染器")
  markdown("修正了傳統「盲目堆疊」導致的導體懸空錯誤。本引擎採用**「介電背景包覆」與「金屬嵌入拓樸」**演算法。")
