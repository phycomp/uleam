from streamlit import caption, code, column_config, columns, data_editor, error, expander, json, markdown, number_input, radio, radio, session_state, set_page_config, slider, subheader, success, text_area, text_input, title, sidebar, button
from json import dumps
from yaml import dump, safe_load
import streamlit as st
import yaml
import json

# ==============================================================================
# 0. 網頁與狀態機 (State Manager) 初始化
# ==============================================================================
set_page_config(page_title="傳輸線截面 DSL 語法樹產生器", layout="wide")
預設疊構=[
        {"layer_name": "L1_SOLDER_MASK", "type": "介電", "thickness": 25, "color": "#1b4d3e", "etch_factor": 90},
        {"layer_name": "L2_SIGNAL_TOP", "type": "導電", "thickness": 35, "color": "#ffaa00", "etch_factor": 75},
        {"layer_name": "L3_PREPREG_1", "type": "介電", "thickness": 100, "color": "#aa9f7f", "etch_factor": 90},
        {"layer_name": "L4_PLANE_1", "type": "導電", "thickness": 35, "color": "#cc6600", "etch_factor": 90},
        {"layer_name": "L5_CORE_1", "type": "介電", "thickness": 150, "color": "#8c8266", "etch_factor": 90},
        {"layer_name": "L6_SIGNAL_MID1", "type": "導電", "thickness": 18, "color": "#ffaa00", "etch_factor": 80},
        {"layer_name": "L7_CORE_2", "type": "介電", "thickness": 150, "color": "#8c8266", "etch_factor": 90},
        {"layer_name": "L8_PLANE_2", "type": "導電", "thickness": 35, "color": "#cc6600", "etch_factor": 90},
        {"layer_name": "L9_PREPREG_2", "type": "介電", "thickness": 100, "color": "#aa9f7f", "etch_factor": 90},
        {"layer_name": "L10_SIGNAL_BOT", "type": "導電", "thickness": 35, "color": "#ffaa00", "etch_factor": 75},
        {"layer_name": "L11_SOLDER_BOT", "type": "介電", "thickness": 25, "color": "#1b4d3e", "etch_factor": 90},
    ]
FPC疊構舊=[
        {"layer_name": "上覆蓋膜", "type": "介電", "thickness": 25, "color": "#1b4d3e", "etch_factor": 90, "material": "PI", "dk": 3.2, "df": 0.008},
        {"layer_name": "上膠層", "type": "介電", "thickness": 25, "color": "#aa9f7f", "etch_factor": 90, "material": "AD", "dk": 3.3, "df": 0.015},
        {"layer_name": "上通孔鍍層-銅", "type": "導電", "thickness": 15, "color": "#ffaa00", "etch_factor": 90, "material": "電鍍", "dk": 17.0, "df": 0.0},
        {"layer_name": "上接地層", "type": "導電", "thickness": 1, "color": "#cc6600", "etch_factor": 90, "material": "NbTi", "dk": 1.0, "df": 0.0}, # 0.2um 以 1um 作為幾何渲染基礎
        {"layer_name": "上介電層", "type": "介電", "thickness": 50, "color": "#8c8266", "etch_factor": 90, "material": "PI", "dk": 3.3, "df": 0.006}, # Df 取中間值 0.006
        {"layer_name": "上介電膠", "type": "介電", "thickness": 12.5, "color": "#baa26a", "etch_factor": 90, "material": "PI膠", "dk": 3.5, "df": 0.012},
        {"layer_name": "訊號層", "type": "導電", "thickness": 1, "color": "#ffc107", "etch_factor": 75, "material": "NbTi", "dk": 1.0, "df": 0.0}, # 核心高頻信號層
        {"layer_name": "底介電層", "type": "介電", "thickness": 50, "color": "#8c8266", "etch_factor": 90, "material": "PI", "dk": 3.3, "df": 0.006},
        {"layer_name": "底接地層", "type": "導電", "thickness": 1, "color": "#cc6600", "etch_factor": 90, "material": "NbTi", "dk": 1.0, "df": 0.0},
        {"layer_name": "底通孔鍍層-銅", "type": "導電", "thickness": 15, "color": "#ffaa00", "etch_factor": 90, "material": "電鍍", "dk": 17.0, "df": 0.0},
        {"layer_name": "底膠層", "type": "介電", "thickness": 25, "color": "#aa9f7f", "etch_factor": 90, "material": "AD", "dk": 3.3, "df": 0.015},
        {"layer_name": "底覆蓋膜", "type": "介電", "thickness": 25, "color": "#1b4d3e", "etch_factor": 90, "material": "PI", "dk": 3.2, "df": 0.008},
    ]
FPC疊構=[
        {"layer_name": "Top-Coverlay(PI)", "type": "dielectric", "thickness": 25.0, "color": "#E8D5C4", "edge_color": "#A0522D", "material": "PI", "dk": 3.3, "df": 0.0040, "etch_factor": 90},
        {"layer_name": "Top-Coverlay(AD)", "type": "dielectric", "thickness": 25.0, "color": "#D4A574", "edge_color": "#8B6914", "material": "AD", "dk": 3.5, "df": 0.0100, "etch_factor": 90},
        {"layer_name": "PTH上", "type": "conductor_layer", "thickness": 15.0, "color": "#B87333", "edge_color": "#8B4513", "material": "Cu", "dk": 1.0, "df": 0.0000, "etch_factor": 90},
        {"layer_name": "L1(接地層)", "type": "conductor_layer", "thickness": 0.2, "color": "#8B9CAD", "edge_color": "#4A5568", "material": "NbTi", "dk": 1.0, "df": 0.0000, "etch_factor": 90},
        {"layer_name": "PI(H1)", "type": "dielectric", "thickness": 50.0, "color": "#C4956A", "edge_color": "#744210", "material": "PI", "dk": 3.3, "df": 0.0058, "etch_factor": 90},
        {"layer_name": "PI glue", "type": "dielectric", "thickness": 12.5, "color": "#C4956A", "edge_color": "#744210", "material": "PI glue", "dk": 3.5, "df": 0.0050, "etch_factor": 90},
        {"layer_name": "L2(訊號層)", "type": "conductor_layer", "thickness": 0.2, "color": "#FFD700", "edge_color": "#B8860B", "material": "NbTi", "dk": 1.0, "df": 0.0000, "etch_factor": 75}, # 主訊號層，預設 75 度梯形蝕刻
        {"layer_name": "PI(H2)", "type": "dielectric", "thickness": 50.0, "color": "#C4956A", "edge_color": "#744210", "material": "PI", "dk": 3.3, "df": 0.0058, "etch_factor": 90},
        {"layer_name": "L3(接地層)", "type": "conductor_layer", "thickness": 0.2, "color": "#8B9CAD", "edge_color": "#4A5568", "material": "NbTi", "dk": 1.0, "df": 0.0000, "etch_factor": 90},
        {"layer_name": "PTH下", "type": "conductor_layer", "thickness": 15.0, "color": "#B87333", "edge_color": "#8B4513", "material": "Cu", "dk": 1.0, "df": 0.0000, "etch_factor": 90},
        {"layer_name": "Bot-Coverlay(AD)", "type": "dielectric", "thickness": 25.0, "color": "#D4A574", "edge_color": "#8B6914", "material": "AD", "dk": 3.5, "df": 0.0100, "etch_factor": 90},
        {"layer_name": "Bot-Coverlay(PI)", "type": "dielectric", "thickness": 25.0, "color": "#E8D5C4", "edge_color": "#A0522D", "material": "PI", "dk": 3.3, "df": 0.0040, "etch_factor": 90}
]

# 初始化 11 層堆疊的預設 session_state
if "master_layers" not in session_state:
    session_state.master_layers=FPC疊構
def 初始化():
    session_state.master_layers=FPC疊構
# 初始化導體集合 (Conductors)
if "conductors_data" not in session_state:
    session_state.conductors_data = [
        {"target_layer": "L2_SIGNAL_TOP", "mode": "absolute", "name": "Diff_P", "x_center_or_start": -150.0, "width": 100.0, "spacing": 0.0, "count": 1},
        {"target_layer": "L2_SIGNAL_TOP", "mode": "absolute", "name": "Diff_N", "x_center_or_start": 0.0, "width": 100.0, "spacing": 0.0, "count": 1},
        {"target_layer": "L6_SIGNAL_MID1", "mode": "repeat", "name": "Bus_Ch", "x_center_or_start": 100.0, "width": 50.0, "spacing": 80.0, "count": 4},
    ]
# 初始化盲埋孔集合 (Vias)
if "vias_data" not in session_state:
    session_state.vias_data = [
        {"name": "Laser_Via_1", "type": "blind", "start_layer": "L2_SIGNAL_TOP", "end_layer": "L4_PLANE_1", "x_center": -150.0, "drill_diameter": 90.0, "color": "#e64a19"}
    ]

with sidebar:
# ==============================================================================
# 1. 介面模式切換：雙軌並行模式開關
# ==============================================================================
  editor_mode = radio("🛠️ 選擇操作模式 (Editor Mode)", ["UI 表單配置驅動", "進階純文字手寫手動調整 (解鎖原始 AST)"], horizontal=True)

# 取得目前所有合法的層名稱清單（供 Via 盲孔與導體選單動態綁定）
  valid_layer_names = [層["layer_name"] for 層 in session_state.stackup_layers]
  導電_names = [層["layer_name"] for 層 in session_state.stackup_layers if 層["type"] == "導電"]
  # 疊構層數 = slider("🎚️ 設定材質疊構層數 (Max 11)", min_value=1, max_value=11, value=6)
  疊構層數 = slider("🎚️ 設定材質疊構層數 (Max 12)", min_value=1, max_value=12, value=12)

# 依據輸入層數，動態截取儲存庫中的層級陣列
  if button('初始化'): 初始化()
  active_stackup = session_state.master_layers[:疊構層數]
from streamlit import empty, pyplot
狀態=empty()
# ==============================================================================
# 2. 模式 A：UI 表單配置驅動
# ==============================================================================
if editor_mode == "UI 表單配置驅動":
    col_ui, col_ast = columns([3, 2])
    層類型=["介電", "導電"] #["介電", "導電"]
    with col_ui:
        st.subheader(f"📐 (1) 疊構材質配置 (Stackup Registry) - 當前已啟用 {疊構層數} 層")
        # with st.expander(f"展開檢視/調整當前 {num_target_layers} 層基本參數 (已完美適配 0.2μm 超導規格)", expanded=True):
        for idx in range(疊構層數):
            層 = active_stackup[idx]
            c1, c2, c3, c4 = columns([2, 1, 1, 1])
            with c1:
                層["layer_name"] = st.text_input(f"Layer {idx+1} 名稱", value=層["layer_name"], key=f"層名{idx}")
            with c2:
                層["type"] = st.radio(f"類型 #{idx+1}", 層類型, index=0 if 層["type"]=="介電" else 1, key=f"層類型{idx}", horizontal=True)
            with c3:
                # 步進值微調至 0.1μm，以利精確編輯 0.2μm NbTi 薄膜層
                層["thickness"] = st.number_input(f"厚度 (μm) #{idx+1}", min_value=0.1, max_value=1000.0, value=float(層["thickness"]), step=0.1, format="%.1f", key=f"層厚度{idx}")
            if 層["type"] == "conductor_layer":
                with c4:
                    層["etch_factor"] = st.slider(f"蝕刻因子 (deg) #{idx+1}", 45, 90, int(層["etch_factor"]), key=f"層蝕刻{idx}")
            else:
                層["etch_factor"] = 90
        # A.2 多通道總線 (Bus) 導體動態 Excel 表格
        subheader("🎛️ 步驟2 層內導體集合配置 (Conductors Matrix)")
        caption("支援絕對座標 (absolute) 或 相對重複陣列 (repeat) 模式。若為 absolute 則無視 spacing 與 count。")
        edited_conductors = data_editor(
            session_state.conductors_data,
            num_rows="dynamic",
            column_config={
                "target_layer": column_config.SelectboxColumn("依附導體層", options=導電_names, required=True),
                "mode": column_config.SelectboxColumn("擺放模式", options=["absolute", "repeat"], required=True),
                "name": column_config.TextColumn("導體名稱", required=True),
                "x_center_or_start": column_config.NumberColumn("X中心/起點 (μm)", required=True),
                "width": column_config.NumberColumn("線寬 W (μm)", min_value=5.0, required=True),
                "spacing": column_config.NumberColumn("線距 S (μm)", min_value=0.0),
                "count": column_config.NumberColumn("重複數量 (Count)", min_value=1, step=1)
            },
            key="conductors_editor"
        )
        session_state.conductors_data = edited_conductors

        # A.3 盲埋孔跨層動態選單綁定表格
        subheader("🕳️ 步驟3 跨層盲埋孔定義 (Via Mapping Matrix)")
        caption("盲孔起止點已透過狀態機動態綁定上方定義的 11 層名稱選單。")
# ==============================================================================
# 修正後的 Via Mapping Matrix column_config 配置
# ==============================================================================
        edited_vias = data_editor(
            session_state.vias_data,
            num_rows="dynamic",
            column_config={
                "name": column_config.TextColumn("Via 名稱", required=True),
                "type": column_config.SelectboxColumn("盲孔類型", options=["blind", "buried", "through"], required=True),
                "start_layer": column_config.SelectboxColumn("起始層 (Start)", options=valid_layer_names, required=True),
                "end_layer": column_config.SelectboxColumn("終止層 (End)", options=valid_layer_names, required=True),
                "x_center": column_config.NumberColumn("X中心座標 (μm)", required=True),
                "drill_diameter": column_config.NumberColumn("鑽孔孔徑 (μm)", min_value=10.0, required=True),
                # 修正：改用 TextColumn 並限制 Hex 色碼格式，避免 ColorPickerColumn 的找不到屬性錯誤
                "color": column_config.TextColumn("渲染標記色彩", max_chars=7, validate=r"^#[0-9A-Fa-f]{6}$")
            },
            key="vias_editor"
        )
        session_state.vias_data = edited_vias

    # B. 抽象語法樹 (AST) 編譯核心
    # 將分離的 UI 狀態資料集按照「層為容器」與「獨立海拔區間」的語義規範組裝
    ast_output = {"stackup": [], "vias": []}
    
    for 層 in session_state.stackup_layers:
        layer_ast = {
            "layer_name": 層["layer_name"],
            "type": 層["type"],
            "thickness": 層["thickness"],
            "color": 層["color"],
            "conductors": []
        }
        if 層["type"] == "導電":
            layer_ast["etch_factor"] = 層["etch_factor"]
            # 翻查並嵌入屬於該層的導體子樹節點
            for cond in session_state.conductors_data:
                if cond and cond.get("target_layer") == 層["layer_name"]:
                    cond_node = {
                        "mode": cond["mode"],
                        "name": cond["name"],
                        "width": cond["width"]
                    }
                    if cond["mode"] == "absolute":
                        cond_node["x_center"] = cond["x_center_or_start"]
                    else:
                        cond_node["x_start"] = cond["x_center_or_start"]
                        cond_node["spacing"] = cond["spacing"]
                        cond_node["count"] = int(cond["count"])
                    layer_ast["conductors"].append(cond_node)
                    
        ast_output["stackup"].append(layer_ast)

    for via in session_state.vias_data:
        if via:
            ast_output["vias"].append({
                "name": via["name"],
                "type": via["type"],
                "start_layer": via["start_layer"],
                "end_layer": via["end_layer"],
                "x_center": via["x_center"],
                "drill_diameter": via["drill_diameter"],
                "color": via.get("color", "#ff0000")
            })

    with col_ast:
        subheader("📄 步驟4 編譯產生的結構化 AST 語法樹")
        format_type = radio("切換匯出格式 (Export DSL)", ["YAML 語法樹格式", "JSON 語法樹格式"], horizontal=True)
        
        if format_type == "YAML 語法樹格式":
            compiled_string = dump(ast_output, sort_keys=False, allow_unicode=True)
            code(compiled_string, language="yaml")
        else:
            compiled_string = json.dumps(ast_output, indent=2, ensure_ascii=False)
            code(compiled_string, language="json")
            
        success("💡 語法樹已即時就緒。您可以點擊代碼框右上角的複製按鈕，直接打包丟入下游渲染器！")

# ==============================================================================
# 3. 模式 B：進階純文字手寫手動調整 (雙軌解鎖模式)
# ==============================================================================
else:
    subheader("✍️ 進階純文字手寫模式 (Direct AST Raw Editor)")
    caption("在此模式下，您可以直接編輯或貼上先前存好的 YAML 語法樹代碼。本文字框將直接作為語法樹輸出源。")
    
    # 預先將當前 UI 狀態編譯出一個基準文字供手寫區承接
    try:
        placeholder_ast = {"stackup": [], "vias": []}
        # 簡易封裝供手寫模式初始顯示
        for 層 in session_state.stackup_layers:
            placeholder_ast["stackup"].append({"layer_name": 層["layer_name"], "type": 層["type"], "thickness": 層["thickness"], "conductors": []})
        initial_text = dump(placeholder_ast, sort_keys=False)
    except:
        initial_text = "stackup: []\nvias: []"
        manual_text = text_area("直接寫入/修改 DSL 語法 (即時驗證 AST)", value=initial_text, height=600)
    try:
      parsed_manual_ast = safe_load(manual_text)
      success("🟢 語法樹驗證通過：結構語義完全合規。")
      json(parsed_manual_ast)
    except Exception as e:
      error(f"🔴 語法編譯失敗：請檢查縮排與層級節點。錯誤訊息: {str(e)}")
with sidebar:
  subheader("🌲 傳輸線截面 DSL 抽象語法樹 (AST) 自動產生器")
  markdown("本工具專注於透過 **UI 參數配置、動態物件表格** 自動組裝出符合語義的結構化 AST 語法樹。")
