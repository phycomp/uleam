from streamlit import columns, json, markdown, pyplot, set_page_config, sidebar, subheader, title, warning, radio, text_input, text_area, json as stJson, error
from matplotlib.pyplot import subplots
from numpy import array, radians, tan
from json import dumps as jsnDumps, loads as jsnLoads
from yaml import safe_load
# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt
import matplotlib.patches as patches
import yaml
import json

# ==============================================================================
# 0. 網頁基本配置
# ==============================================================================
set_page_config(page_title="通用型傳輸線截面 DSL 向量渲染器", layout="wide")

# ==============================================================================
# 1. 預設的通用型層級化 DSL 範本 (YAML 格式，清晰展現 AST 拓樸結構)
# ==============================================================================
預設DSL = """# 通用型傳輸線與盲埋孔截面 DSL 語法樹定義
stackup:
  - layer_name: "TOP_SOLDER"
    type: "dielectric"
    thickness: 20
    color: "#2e5c1e" # 深綠色阻焊層
    conductors: []

  - layer_name: "L1_SIGNAL"
    type: "conductor_layer"
    thickness: 35
    etch_factor: 70 # 梯形側邊斜角度 (度)
    color: "#ffc107" # 金黃/紅銅色
    conductors:
      - mode: "absolute"
        name: "Trace_A"
        x_center: -200
        width: 120
      - mode: "repeat"
        name: "Bus_Line"
        x_start: 0
        width: 80
        spacing: 100
        count: 3

  - layer_name: "DIELECTRIC_1"
    type: "dielectric"
    thickness: 150
    color: "#b0a88a" # 介電質草黃色
    conductors: []

  - layer_name: "L2_PLANE"
    type: "conductor_layer"
    thickness: 35
    etch_factor: 90 # 完美矩形參考地平面
    color: "#cc7a00"
    conductors:
      - mode: "absolute"
        name: "GND_Plane"
        x_center: 0
        width: 1200

# 盲埋孔 (Via) 集合定義
vias:
  - name: "Blind_Via_1"
    type: "blind"
    start_layer: "L1_SIGNAL"
    end_layer: "L2_PLANE"
    x_center: -200
    drill_diameter: 100
    pad_diameter: 160
    color: "#e65100"
"""

with sidebar:
# ==============================================================================
# 2. 側邊欄：互動式 UI 與 DSL 抽象樹編輯區
# ==============================================================================
  subheader("🛠️ 1. DSL 抽象語法樹結構編輯器")
  語法 = radio("編輯風格", ["YAML (層級清晰)", "JSON (語法嚴謹)"], horizontal=True, index=0)

  from streamlit_monaco_yaml import monaco_editor
  from streamlit_monaco import st_monaco
# ==============================================================================
# 3. 核心抽象層引擎：將 AST 語法樹轉換為絕對幾何多邊形頂點
# ==============================================================================
def 通用截面(ast):
    """
    實作真正的 Lexer/Parser 抽象層：將層級化容器結構拉平並解算為絕對 Y 軸高度與 Polygon 頂點集合
    """
    if not ast or "stackup" not in ast:
        return {}, [], []

    layer_y_map = {} # 記錄各層的底與頂 Y 軸座標，供 Via 盲孔查詢
    geom_layers = []
    geom_conductors = []
    geom_vias = []
    
    current_y = 0.0 # 自底向上疊加
    
    # 步驟 1：解算層容器拓樸 (由底層向上逆向或順向掃描，此處採 DSL 定義順序由上至下解算，故先反轉)
    reversed_stackup = list(reversed(ast["stackup"]))
    
    for layer in reversed_stackup:
        l_name = layer["layer_name"]
        l_type = layer["type"]
        thick = float(layer.get("thickness", 0))
        l_color = layer.get("color", "#ffffff")
        etch_angle = float(layer.get("etch_factor", 90))
        
        y_bot = current_y
        y_top = current_y + thick
        layer_y_map[l_name] = {"bot": y_bot, "top": y_top}
        
        # 建立介電層背景多邊形頂點 (覆蓋大範圍 -1000 到 +1000 um)
        if l_type == "dielectric":
            v_dielectric = array([[-1000, y_bot], [1000, y_bot], [1000, y_top], [-1000, y_top]])
            geom_layers.append({"name": l_name, "poly": v_dielectric, "color": l_color})
            
        # 步驟 2：解算導體排列模式 (絕對座標 vs 相對重複)
        if "conductors" in layer:
            for cond in layer["conductors"]:
                mode = cond.get("mode", "absolute")
                w_nominal = float(cond.get("width", 50))
                
                # 解算位置清單
                x_centers = []
                if mode == "absolute":
                    x_centers.append(float(cond.get("x_center", 0)))
                elif mode == "repeat":
                    x_start = float(cond.get("x_start", 0))
                    spacing = float(cond.get("spacing", 100))
                    count = int(cond.get("count", 1))
                    for c in range(count):
                        x_centers.append(x_start + c * spacing)
                        
                # 步驟 3：依據蝕刻因子 (Etch Factor) 計算導體的梯形多邊形頂點 (非矩形化)
                for x_c in x_centers:
                    # 計算因梯形傾斜產生的頂寬與底寬微調
                    if etch_angle < 90:
                        rad = radians(etch_angle)
                        delta_x = thick / tan(rad)
                        w_bot = w_nominal + delta_x
                        w_top = w_nominal - delta_x
                    else:
                        w_bot = w_nominal
                        w_top = w_nominal
                        
                    # 梯形四個頂點的向量順序 (順時針)
                    v_cond = array([
                        [x_c - w_bot/2, y_bot], # 左下
                        [x_c + w_bot/2, y_bot], # 右下
                        [x_c + w_top/2, y_top], # 右上
                        [x_c - w_top/2, y_top]  # 左上
                    ])
                    geom_conductors.append({"name": cond.get("name", "Trace"), "poly": v_cond, "color": l_color})
                    
        current_y = y_top # 堆疊指針向上推
        
    # 步驟 4：解算盲埋孔 (Via Sub-AST) 到絕對層次高度的映射
    if "vias" in ast and ast["vias"]:
        for via in ast["vias"]:
            s_lay = via.get("start_layer")
            e_lay = via.get("end_layer")
            x_via = float(via.get("x_center", 0))
            d_drill = float(via.get("drill_diameter", 50))
            v_color = via.get("color", "#ff0000")
            
            # 從層映射表抓取精確的縱向邊界
            if s_lay in layer_y_map and e_lay in layer_y_map:
                y1 = layer_y_map[s_lay]["bot"]
                y2 = layer_y_map[e_lay]["top"]
                y_v_bot = min(y1, y2)
                y_v_top = max(y1, y2)
                
                # 盲孔在截面上以多邊形（中空管狀或實心矩形柱）向量渲染
                v_via = array([
                    [x_via - d_drill/2, y_v_bot],
                    [x_via + d_drill/2, y_v_bot],
                    [x_via + d_drill/2, y_v_top],
                    [x_via - d_drill/2, y_v_top]
                ])
                geom_vias.append({"name": via["name"], "poly": v_via, "color": v_color})
                
    return layer_y_map, geom_layers, geom_conductors, geom_vias

def 渲染雅模(dsl_format=語法):
  if dsl_format == "YAML (層級清晰)":
    # raw_dsl_text = text_area("編輯 DSL 文字 (即時驅動 AST)", 預設DSL, height=550)
    raw_dsl_text = st_monaco(預設DSL, height=1000, language='yaml')  #key="monaco_editor", schema=預設DSL,  a unique key avoids to reload the editor each time the content changed
    try:
        ast_structure = safe_load(raw_dsl_text)
        is_valid = True
    except Exception as e:
        error(f"❌ YAML 解析錯誤: {str(e)}")
        is_valid = False
  else:
    # 轉換成 JSON 當作展示
    try:
        initial_json = jsnDumps(safe_load(預設DSL), indent=2)
    except:
        initial_json = "{}"
    raw_dsl_text = text_area("編輯 DSL 文字 (即時驅動 AST)", initial_json, height=550)
    try:
        ast_structure = jsnLoads(raw_dsl_text)
        is_valid = True
    except Exception as e:
        error(f"❌ JSON 解析錯誤: {str(e)}")
        is_valid = False
  return ast_structure
# ==============================================================================
# 4. 網頁渲染佈局
# ==============================================================================

# if is_valid:
    # 驅動 Parser 引擎
ast_structure=渲染雅模(dsl_format=語法)
y_map, layers, conductors, vias = 通用截面(ast_structure)

col_main, col_tree = columns([3, 1])

with col_main:
    subheader("🖼️ 2. Matplotlib 向量多邊形高解析度渲染 (通用截面)")
    
    # 建立高客製化圖表
    fig, ax = subplots(figsize=(10, 5))
    ax.set_facecolor("#1a1a1a") # 深色網格底色，烘托 EDA 工具感
    
    # 1. 渲染背景介電層
    for lay in layers:
        polygon = patches.Polygon(lay["poly"], closed=True, facecolor=lay["color"], edgecolor="#555555", alpha=0.8, linewidth=0.5, label=lay["name"])
        ax.add_patch(polygon)
        
    # 2. 渲染金屬傳輸線導體 (金黃與紅銅防線)
    for cond in conductors:
        polygon = patches.Polygon(cond["poly"], closed=True, facecolor=cond["color"], edgecolor="#ffffff", linewidth=1.2, zorder=3)
        ax.add_patch(polygon)
        
    # 3. 渲染盲埋孔 Via 通道
    for via in vias:
        polygon = patches.Polygon(via["poly"], closed=True, facecolor=via["color"], edgecolor="#ffffff", hatch='//', linewidth=1.0, zorder=4)
        ax.add_patch(polygon)
        
    # 4. 加入微米 (μm) 專業尺度標記線與視覺優化
    ax.set_xlim(-450, 450)
    # 動態計算高度極限以利 Auto-scaling
    max_y = max([vals["top"] for vals in y_map.values()]) if y_map else 300
    ax.set_ylim(-20, max_y + 30)
    
    ax.set_xlabel("橫向中心寬度 Width (μm)", fontsize=10)
    ax.set_ylabel("縱向堆疊高度 Height (μm)", fontsize=10)
    ax.grid(True, which='both', color='#444444', linestyle=':', linewidth=0.5)
    ax.tick_params(colors='#333333', labelsize=9)
    
    pyplot(fig)
    
with col_tree:
    subheader("🌲 3. 解算後的 AST 語法樹物件")
    stJson(ast_structure)
# else:
    # warning("⚠️ 請在側邊欄修正語法錯誤，以啟用多邊形渲染工作流。")

with sidebar:
  subheader("🗺️ 通用型傳輸線截面 DSL 抽象語法樹 (AST) 向量渲染器")
  markdown("本系統採用**「層為容器」**的拓樸結構、**「多邊形頂點 (Polygon)」**渲染引擎，支援任意多層堆疊、盲埋孔與梯形蝕刻因子。")
