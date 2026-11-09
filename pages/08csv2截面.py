from streamlit import code, columns, info, markdown, pyplot, session_state, set_page_config, sidebar, subheader, title, file_uploader, text_area, error, success, checkbox
from matplotlib.pyplot import subplots
from pandas import read_csv
from numpy import array, radians, tan
from yaml import dump
from 疊構Util import csv2ast, 疊構解析II
# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt
import matplotlib.patches as patches
# import pandas as pd
# import yaml
from io import StringIO

# ==============================================================================
# 0. 網頁基本配置與狀態機初始化
# ==============================================================================
set_page_config(page_title="FPC 疊構自動化編譯與渲染器", layout="wide")
with sidebar:
  subheader("🚀 FPC 疊構自動化編議與向量多邊形渲染器")
  markdown(r"本系統實現：**[CSV 結構輸入/貼上]** $\rightarrow$ **[自動生成 YAML AST 語法樹]** $\rightarrow$ **[嵌入式硬體拓樸渲染]** 的全自動化 Pipeline。")

# 初始化預設的導體集合與盲孔資料 (供 AST 編譯時自動嵌入訊號層)
if "conductors_preset" not in session_state:
    session_state.conductors_preset = [
        {"mode": "absolute", "name": "RF_Trace_P", "x_center": -120.0, "width": 50.0},
        {"mode": "absolute", "name": "RF_Trace_N", "x_center": 20.0, "width": 50.0},
        {"mode": "repeat", "name": "Bus_Array", "x_start": 180.0, "width": 40.0, "spacing": 70.0, "count": 3}
    ]

# 預設的 FPC 12層 CSV 範本文字 (供使用者直接複製、貼上或測試)
CSV_TEMPLATE = """名稱,厚度um,材料,DK,DF,顏色,邊緣,是訊號層
Top-Coverlay(PI),25,PI,3.3,0.004,#E8D5C4,#A0522D,False
Top-Coverlay(AD),25,AD,3.5,0.01,#D4A574,#8B6914,False
PTH上,15,Cu,1.0,0.0,#B87333,#8B4513,False
L1(接地層),0.2,NbTi,1.0,0.0,#8B9CAD,#4A5568,False
PI(H1),50,PI,3.3,0.0058,#C4956A,#744210,False
PI glue,12.5,PI glue,3.5,0.005,#C4956A,#744210,False
L2(訊號層),0.2,NbTi,1.0,0.0,#FFD700,#B8860B,True
PI(H2),50,PI,3.3,0.0058,#C4956A,#744210,False
L3(接地層),0.2,NbTi,1.0,0.0,#8B9CAD,#4A5568,False
PTH下,15,Cu,1.0,0.0,#B87333,#8B4513,False
Bot-Coverlay(AD),25,AD,3.5,0.01,#D4A574,#8B6914,False
Bot-Coverlay(PI),25,PI,3.3,0.004,#E8D5C4,#A0522D,False"""

with sidebar:
# ==============================================================================
# 1. Pipeline 階段一：雙軌資料輸入管道 (上傳 / 貼上 CSV)
# ==============================================================================
  subheader("📁 階段 1：疊構 CSV 資料輸入")
# input_method = radio("選擇輸入管道", ["管道 1：上傳 CSV 檔案", "管道 2：直接貼上 CSV 內容"])

  資框 = None

# if input_method == "管道 1：上傳 CSV 檔案":
  if checkbox('上傳csv'):
    uploaded_file = file_uploader("請選擇疊構 CSV 檔案", type=["csv"])
    if uploaded_file is not None:
      try:
          資框 = read_csv(uploaded_file)
          success("🟢 檔案上傳並解析成功！")
      except Exception as e:
          error(f"🔴 CSV 讀取失敗: {str(e)}")
  else:
    markdown("### 📋 貼上區")
    raw_csv_paste = text_area("請貼上 CSV 文字內容 (預設已載入 FPC 12層規格)", CSV_TEMPLATE, height=350)
    if raw_csv_paste.strip():
        try:
            資框 = read_csv(StringIO(raw_csv_paste.strip()))
            success("🟢 貼上內容解析成功！")
        except Exception as e:
            error(f"🔴 貼上內容語法錯誤: {str(e)}")
    資框

# ==============================================================================
# 4. 主畫面：自動化 Pipeline 結果雙視窗呈現
# ==============================================================================
if 資框 is not None:
    # 執行轉譯 Pipeline 核心
    語法樹 = csv2ast(資框)
    # 語法樹
    y_reg, dielectrics, conductors, vias = 疊構解析II(語法樹)
    
    col_vis, col_ast = columns([3, 2])
    
    with col_vis:
        subheader("🖼️ 階段 3：Matplotlib 通用向量幾何截面圖")
        
        # 繪置高階 EDA 對比配色網格
        fig, ax = subplots(figsize=(11, 6))
        ax.set_facecolor("#121212") # 暗色底色
        
        # 1. 繪製背景包覆的介電層
        for di in dielectrics:
          ax.add_patch(patches.Polygon(di["poly"], closed=True, facecolor=di["color"], edgecolor=di["edge_color"], alpha=0.9, linewidth=1.0))
        # 於右側對齊標記實體層名稱
          ax.text(480, (di["poly"][0, 1] + di["poly"][2, 1])/2, di["name"], color="#A0A0A0", va="center", fontsize=8, fontweight="bold")
        # 2. 繪製金屬傳輸線與接地平面 (嵌入包覆)
        for co in conductors:
          ax.add_patch(patches.Polygon(co["poly"], closed=True, facecolor=co["color"], edgecolor=co["edge_color"], linewidth=1.2, zorder=3))
        # 3. 繪製斜紋填充盲孔
        for vi in vias:
          ax.add_patch(patches.Polygon(vi["poly"], closed=True, facecolor=vi["color"], edgecolor="#ffffff", hatch='//', linewidth=1.0, zorder=4))
          ax.text(vi["poly"][0, 0] - 10, (vi["poly"][0, 1] + vi["poly"][2, 1])/2, vi["name"], color="#ffffff", ha="right", va="center", fontsize=8, zorder=5)
        # 畫布幾何尺度美化 (微米標記軸)
        ax.set_xlim(-450, 620)
        max_h = max([v["top"] for v in y_reg.values()]) if y_reg else 300
        ax.set_ylim(-10, max_h + 20)
        ax.set_xlabel("橫向坐標 Width (μm)", fontsize=10)
        ax.set_ylabel("縱向實體海拔高度 Height (μm)", fontsize=10)
        ax.grid(True, color="#252525", linestyle=":", linewidth=0.5)
        pyplot(fig)
    with col_ast:
      subheader("🌲 階段 2：自動編譯轉換出的 YAML AST 語法樹")
      yaml_string = dump(語法樹, sort_keys=False, allow_unicode=True)
      code(yaml_string, language="yaml")
      info("💡 這個 YAML 語法樹是由上傳/貼上的 CSV 數據自動解析出來的，您可直接將其複製運用於下游的 EM 求解器。")
else:
  info("💡 請在側邊欄[上傳 CSV 檔案]或[直接貼上 CSV 內容]，系統將會自動執行一鍵轉譯與截面渲染。")
