from numpy import array, radians, tan
from pandas import notna, read_csv
from streamlit import session_state
# ==============================================================================
# 2. 核心 Parser 抽象層：導正硬體幾何海拔的解算引擎
# ==============================================================================
# 疊構解析 已統一至 疊構解析II（保留舊名稱相容）
def 疊構解析(ast):
    return 疊構解析II(ast)
# ==============================================================================
# 2. Pipeline 階段二：CSV 轉成結構化 YAML AST 語法樹
# ==============================================================================
def csv2ast(df):  #compile_csv_to_yaml_ast
    """
    語義解析器：將拉平的 CSV 結構轉化為包含硬體層級容器的 YAML AST
    """
    if df is None or df.empty:
        return None
        
    ast = {"stackup": [], "vias": []}
    
    # """名稱,厚度um,材料,DK,DF,顏色,邊緣,是訊號層
    # 遍歷 CSV 各行資料
    for idx, row in df.iterrows():
        name = str(row["名稱"])
        thick = float(row["厚度um"])
        material = str(row["材料"])
        # 處理布林值判定
        is_signal_layer = str(row["是訊號層"]).strip().lower() in ["true", "1", "yes"]
        
        # 建立層容器節點
        layer_node = {
            "layer_name": name,
            "type": "conductor_layer" if (is_signal_layer or material in ["Cu", "NbTi"]) else "dielectric",
            "thickness": thick,
            "color": str(row["顏色"]),
            "edge_color": str(row["邊緣"]),
            "material": material,
            "dk": float(row["DK"]) if notna(row["DK"]) else 1.0,
            "df": float(row["DF"]) if notna(row["DF"]) else 0.0,
            "conductors": []
        }
        
        # 預設製程幾何：如果是主訊號層，給予 75 度蝕刻因子，其餘金屬給予 90 度完美矩形
        if layer_node["type"] == "conductor_layer":
            layer_node["etch_factor"] = 75 if is_signal_layer else 90
            # [核心整合] 若是主訊號層，自動將預設的多通道 Bus 導體子樹嵌入 AST 節點
            if is_signal_layer:
                layer_node["conductors"] = session_state.conductors_preset
                
        ast["stackup"].append(layer_node)
        
    # 自動補上一組示範盲孔，自動錨定在被判定為訊號層的區間
    signal_layers = [l["layer_name"] for l in ast["stackup"] if l["layer_name"].find("訊號") != -1 or l["layer_name"].find("L2") != -1]
    if signal_layers:
        ast["vias"].append({
            "name": "PTH_Via_1",
            "type": "blind",
            "start_layer": ast["stackup"][2]["layer_name"], # 預設第 3 層
            "end_layer": signal_layers[0],
            "x_center": -120.0,
            "drill_diameter": 40.0,
            "color": "#B87333"
        })
        
    return ast

# ==============================================================================
# 3. Pipeline 階段三：核心嵌入式拓樸幾何多邊形解析引擎 (導正硬體海拔)
# ==============================================================================
def 疊構解析II(ast):
    layer_registry = {}
    geom_dielectrics = []
    geom_conductors = []
    geom_vias = []
    
    if not ast or "stackup" not in ast:
        return layer_registry, [], [], []
        
    current_y = 0.0
    # 工藝疊構由底向上逆向解算多邊形
    reversed_stackup = list(reversed(ast["stackup"]))
    
    for layer in reversed_stackup:
        name = layer["layer_name"]
        l_type = layer["type"]
        thick = float(layer["thickness"])
        color = layer["color"]
        edge_c = layer.get("edge_color", "#333333")
        etch_angle = float(layer.get("etch_factor", 90))
        
        y_bot = current_y
        y_top = current_y + thick
        layer_registry[name] = {"bot": y_bot, "top": y_top}
        
        # 介電層：建立橫向大背景多邊形
        if l_type == "dielectric":
            v_di = array([[-1200, y_bot], [1200, y_bot], [1200, y_top], [-1200, y_top]])
            geom_dielectrics.append({"name": name, "poly": v_di, "color": color, "edge_color": edge_c})
            current_y = y_top
            
        # 導電層：修正硬體拓樸，金屬嵌入背景，指派絕對頂點向量
        elif l_type == "conductor_layer":
            y_metal_bot = current_y
            y_metal_top = current_y + thick
            layer_registry[name] = {"bot": y_metal_bot, "top": y_metal_top}
            
            if "conductors" in layer and layer["conductors"]:
                for cond in layer["conductors"]:
                    mode = cond.get("mode", "absolute")
                    w_nominal = float(cond["width"])
                    
                    x_centers = []
                    if mode == "absolute":
                        x_centers.append(float(cond["x_center"]))
                    elif mode == "repeat":
                        x_start = float(cond["x_start"])
                        spacing = float(cond["spacing"])
                        count = int(cond["count"])
                        for c in range(count):
                            x_centers.append(x_start + c * spacing)
                            
                    # 計算考慮製程側蝕（Etch Factor）的梯形向量
                    for x_c in x_centers:
                        w_bot, w_top = w_nominal, w_nominal
                        if etch_angle < 90:
                            rad = radians(etch_angle)
                            delta = thick / tan(rad)
                            w_bot = w_nominal + delta
                            w_top = w_nominal - delta
                            
                        v_cond = array([
                            [x_c - w_bot/2, y_metal_bot],
                            [x_c + w_bot/2, y_metal_bot],
                            [x_c + w_top/2, y_metal_top],
                            [x_c - w_top/2, y_metal_top]
                        ])
                        geom_conductors.append({"name": cond["name"], "poly": v_cond, "color": color, "edge_color": edge_c})
            else:
                # 參考平面層 (Plane): 連續覆蓋的完整金屬多邊形板塊
                v_plane = array([[-1200, y_metal_bot], [1200, y_metal_bot], [1200, y_metal_top], [-1200, y_metal_top]])
                geom_conductors.append({"name": name, "poly": v_plane, "color": color, "edge_color": edge_c})
                
            current_y = y_metal_top

    # 盲孔垂直跨度海拔解算
    if "vias" in ast and ast["vias"]:
        for via in ast["vias"]:
            s_lay = via["start_layer"]
            e_lay = via["end_layer"]
            x_via = float(via["x_center"])
            d_drill = float(via["drill_diameter"])
            
            if s_lay in layer_registry and e_lay in layer_registry:
                y_v1 = layer_registry[s_lay]["bot"]
                y_v2 = layer_registry[e_lay]["top"]
                y_min, y_max = min(y_v1, y_v2), max(y_v1, y_v2)
                
                v_via = array([
                    [x_via - d_drill/2, y_min],
                    [x_via + d_drill/2, y_min],
                    [x_via + d_drill/2, y_max],
                    [x_via - d_drill/2, y_max]
                ])
                geom_vias.append({"name": via["name"], "poly": v_via, "color": via["color"]})
                
    return layer_registry, geom_dielectrics, geom_conductors, geom_vias




# --- 整合：統一解析器入口（舊名稱指向完整版 II）---
疊構解析 = 疊構解析II
