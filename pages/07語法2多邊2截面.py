from streamlit import columns, json, markdown, pyplot, set_page_config, sidebar, subheader, title, warning
from matplotlib.pyplot import subplots
from numpy import array, radians, tan
from json import dumps, loads
from yaml import safe_load
from 疊構Util import 疊構解析
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import yaml
import json

# ==============================================================================
# 0. 網頁基本配置與 UI 設計
# ==============================================================================
st.set_page_config(page_title="DSL 向量多邊形截面分析儀", layout="wide")
st.title("🎛️ 傳輸線截面 DSL 全自動化多邊形渲染器")
st.markdown(r"本工具完整實作：**[1. 文字語法樹 (AST)]** $\rightarrow$ **[2. 幾何多邊形轉換 (Parser)]** $\rightarrow$ **[3. Matplotlib 向量繪製]** 的端到端流程。")

# ==============================================================================
# 1. 通用型多層堆疊與盲孔 DSL 語法樹範本 (YAML 格式)
# ==============================================================================
DEFAULT_DSL = """# 定義電路板多層堆疊抽象語法樹 (AST Stackup Container)
stackup:
  - layer_name: "L1_SOLDER_MASK"
    type: "dielectric"
    thickness: 25
    color: "#1b4d3e" # 深綠色防焊層
    conductors: []

  - layer_name: "L2_SIGNAL_TOP"
    type: "conductor_layer"
    thickness: 35
    etch_factor: 75 # 梯形側邊斜角度 (度)
    color: "#ffaa00" # 紅銅金黃色
    conductors:
      - mode: "absolute"
        name: "Diff_Pair_P"
        x_center: -150
        width: 100
      - mode: "absolute"
        name: "Diff_Pair_N"
        x_center: 0
        width: 100
      - mode: "repeat"
        name: "Bus_Array"
        x_start: 200
        width: 60
        spacing: 90
        count: 3

  - layer_name: "L3_CORE_DI"
    type: "dielectric"
    thickness: 160
    color: "#aa9f7f" # 介電質草黃色
    conductors: []

  - layer_name: "L4_GND_PLANE"
    type: "conductor_layer"
    thickness: 35
    etch_factor: 90 # 90度代表完美矩形
    color: "#cc6600"
    conductors:
      - mode: "absolute"
        name: "Main_GND"
        x_center: 0
        width: 1200 # 覆蓋整張畫布的參考平面

# 定義盲埋孔 (Via) 集合
vias:
  - name: "Laser_Via_1"
    type: "blind"
    start_layer: "L2_SIGNAL_TOP"
    end_layer: "L4_GND_PLANE"
    x_center: -150
    drill_diameter: 90
    color: "#e64a19" # 盲孔金屬填充色
"""

# ==============================================================================
# 2. 側邊欄：DSL 語法編輯區
# ==============================================================================
st.sidebar.header("📁 1. 編輯文字語法樹 (DSL Text)")
syntax_mode = st.sidebar.radio("語法格式", ["YAML 風格", "JSON 風格"])

if syntax_mode == "YAML 風格":
    raw_text = st.sidebar.text_area("編輯 YAML (即時重繪)", DEFAULT_DSL, height=550)
    try:
        ast_tree = yaml.safe_load(raw_text)
        is_valid = True
    except Exception as e:
        st.sidebar.error(f"❌ YAML 語法解析錯誤: {str(e)}")
        is_valid = False
else:
    # 預先將 YAML 轉為 JSON 供使用者參考
    try: json_init = json.dumps(yaml.safe_load(DEFAULT_DSL), indent=2)
    except: json_init = "{}"
    raw_text = st.sidebar.text_area("編輯 JSON (即時重繪)", json_init, height=550)
    try:
        ast_tree = json.loads(raw_text)
        is_valid = True
    except Exception as e:
        st.sidebar.error(f"❌ JSON 語法解析錯誤: {str(e)}")
        is_valid = False

# ==============================================================================
# 3. 核心 Parser 抽象層：文字語法樹 (AST) 轉換為幾何多邊形頂點
# ==============================================================================
def parse_ast_to_polygons(ast):
    """
    核心解析器：解析層容器拓樸、解算導體排列模式、非矩形化梯形蝕刻，並映射盲孔垂直高度。
    """
    if not ast or "stackup" not in ast:
        return {}, [], [], []

    layer_height_registry = {} # 註冊各層絕對高度範圍，供 Via 盲孔查找
    polygons_dielectric = []
    polygons_conductor = []
    polygons_via = []
    
    # 物理堆疊由底向上計算 (將 DSL 容器由下至上拉平解算)
    current_y = 0.0
    reversed_stackup = list(reversed(ast["stackup"]))
    
    for layer in reversed_stackup:
        l_name = layer["layer_name"]
        l_type = layer["type"]
        thick = float(layer.get("thickness", 0))
        l_color = layer.get("color", "#ffffff")
        etch_angle = float(layer.get("etch_factor", 90))
        
        y_bottom = current_y
        y_top = current_y + thick
        
        # 註冊此層的海拔座標
        layer_height_registry[l_name] = {"bottom": y_bottom, "top": y_top}
        
        # [決策三實作] 建立介電層大背景多邊形 (橫向覆蓋 -1500 到 +1500 um)
        if l_type == "dielectric":
            v_dielectric = np.array([[-1500, y_bottom], [1500, y_bottom], [1500, y_top], [-1500, y_top]])
            polygons_dielectric.append({"name": l_name, "vertices": v_dielectric, "color": l_color})
            
        # [決策二實作] 解析導體佈局模式 (絕對座標 vs 相對重複)
        if "conductors" in layer:
            for cond in layer["conductors"]:
                mode = cond.get("mode", "absolute")
                w_nominal = float(cond.get("width", 50))
                
                # 計算該導體在 X 軸上的所有中心點
                x_positions = []
                if mode == "absolute":
                    x_positions.append(float(cond.get("x_center", 0)))
                elif mode == "repeat":
                    x_start = float(cond.get("x_start", 0))
                    spacing = float(cond.get("spacing", 100))
                    count = int(cond.get("count", 1))
                    for c in range(count):
                        x_positions.append(x_start + c * spacing)
                        
                # [決策一與實作2] 基於蝕刻因子 (Etch Factor) 計算導體的梯形頂點 (非矩形化向量)
                for x_c in x_positions:
                    if etch_angle < 90:
                        rad = np.radians(etch_angle)
                        delta_x = thick / np.tan(rad)
                        w_bot = w_nominal + delta_x
                        w_top = w_nominal - delta_x
                    else:
                        w_bot = w_nominal
                        w_top = w_nominal
                        
                    # 依據順時針建立四邊形多邊形頂點
                    v_conductor = np.array([
                        [x_c - w_bot/2, y_bottom], # 左下
                        [x_c + w_bot/2, y_bottom], # 右下
                        [x_c + w_top/2, y_top],    # 右上
                        [x_c - w_top/2, y_top]     # 左上
                    ])
                    polygons_conductor.append({"name": cond.get("name", "Trace"), "vertices": v_conductor, "color": l_color})
                    
        current_y = y_top # 指針向上堆疊
        
    # [應用場景1實作] 盲埋孔層級縱向映射與多邊形頂點生成
    if "vias" in ast and ast["vias"]:
        for via in ast["vias"]:
            s_layer = via.get("start_layer")
            e_layer = via.get("end_layer")
            x_via = float(via.get("x_center", 0))
            d_drill = float(via.get("drill_diameter", 50))
            v_color = via.get("color", "#ff0000")
            
            # 從註冊表中查詢起點層與終點層的絕對 Y 軸範圍
            if s_layer in layer_height_registry and e_layer in layer_height_registry:
                y1 = layer_height_registry[s_layer]["bottom"]
                y2 = layer_height_registry[e_layer]["top"]
                y_via_min = min(y1, y2)
                y_via_max = max(y1, y2)
                
                # 將盲孔實體化為一組 2D 多邊形柱狀頂點
                v_via = np.array([
                    [x_via - d_drill/2, y_via_min],
                    [x_via + d_drill/2, y_via_min],
                    [x_via + d_drill/2, y_via_max],
                    [x_via - d_drill/2, y_via_max]
                ])
                polygons_via.append({"name": via["name"], "vertices": v_via, "color": v_color})
                
    return layer_height_registry, polygons_dielectric, polygons_conductor, polygons_via
from streamlit import empty, pyplot
狀態=empty()
# ==============================================================================
# 4. 主要工作流展示與 Matplotlib 向量渲染區
# ==============================================================================
col_plot, col_ast = st.columns(2)

if is_valid:
    # 執行底層 Parser Core，將語法樹轉換為純向量幾何
    height_registry, dielectrics, conductors, vias = 疊構解析(ast_tree)
    狀態.code(dielectrics)
    with col_plot:
        st.subheader("🖼️ 2. Matplotlib 幾何多邊形向量渲染 (PCB 橫截面)")
        
        # 實作 EDA 業界標準高對比配色視覺化
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_facecolor("#181818") # 使用 EDA 暗色模式底色，突顯結構線條
        
        # A. 渲染背景介電層 (Layer Container Background)
        for di in dielectrics:
            poly_patch = patches.Polygon(di["vertices"], closed=True, facecolor=di["color"], edgecolor="#444444", alpha=0.85, linewidth=0.5)
            ax.add_patch(poly_patch)
            
        # B. 渲染金屬傳輸線導體 (Conductor Layer) - 真實梯形截面
        for cond in conductors:
            poly_patch = patches.Polygon(cond["vertices"], closed=True, facecolor=cond["color"], edgecolor="#ffffff", linewidth=1.2, zorder=3)
            ax.add_patch(poly_patch)
            
        # C. 渲染盲埋孔金屬柱 (Via Entities)
        for via in vias:
            poly_patch = patches.Polygon(via["vertices"], closed=True, facecolor=via["color"], edgecolor="#ffffff", hatch='//', linewidth=1.0, zorder=4)
            ax.add_patch(poly_patch)
            
        # 尺寸與標記線優化 (加入微米 μm 尺寸刻度)
        ax.set_xlim(-450, 450)
        max_total_y = max([v["top"] for v in height_registry.values()]) if height_registry else 250
        ax.set_ylim(-20, max_total_y + 30)
        
        ax.set_xlabel("橫向中心座標 X Width (μm)", fontsize=10, color="#222222")
        ax.set_ylabel("縱向堆疊海拔 Y Height (μm)", fontsize=10, color="#222222")
        ax.grid(True, which='both', color='#333333', linestyle=':', linewidth=0.5)
        ax.tick_params(colors='#222222', labelsize=9)
        
        st.pyplot(fig)
        
    with col_ast:
        st.subheader("🌲 3. 核心解析出的 AST 數據結構物件 (JSON Tree)")
        st.json(ast_tree)
else:
    st.warning("⚠️ 目前 DSL 語法樹存在錯誤，請依照錯誤提示修正以重新驅動多邊形工作流。")
