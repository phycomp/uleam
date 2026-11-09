from streamlit import button, code, columns, download_button, error, set_page_config, subheader, text_area, title, write
from yaml import safe_load
import streamlit as st
import yaml
from pyaedt import Q3d, Hfss

# ==================== 1. 元件解析工廠 ====================
class AnsysPyAEDTComponent:
    def __init__(self, name, data):
        self.name = name
        self.params = data.get("parameters", {})
        self.ports = data.get("ports", [])
        self.boundaries = data.get("boundaries", [])

    def build_geometry(self, app):
        """由子類別實作幾何建模"""
        raise NotImplementedError

    def assign_electromagnetics(self, app):
        """通用電磁設定：自動綁定 Ports 與 Boundaries"""
        # 處理 Ports
        for port in self.ports:
            if port["type"] == "WavePort":
                # PyAEDT 範例：針對 HFSS/Q3D 幫指定物件建立 Terminal/Port
                # 這裡依據工具類型調用 app.auto_assign_terminals 或 app.create_wave_port
                pass
            elif port["type"] == "Source": # Q3D 專用
                app.assign_source_to_sheet(port["terminal_object"], name=port["name"])

        # 處理 Boundaries
        for bnd in self.boundaries:
            if bnd["type"] == "PerfectE":
                app.assign_perfecte(bnd["target_object"], name=bnd["name"])
            elif bnd["type"] == "Radiation":
                app.assign_radiation_boundary_to_objects(bnd["target_object"], name=bnd["name"])

# 同軸線建模實作
class CoaxialParser(AnsysPyAEDTComponent):
    def build_geometry(self, app):
        p = self.params
        # 使用 PyAEDT 原生幾何指令建立圓柱體
        inner = app.modeler.create_cylinder(
            cs_axis="Z", position=[0, 0, 0], radius=p["inner_radius"], height=50,
            name=f"{self.name}_inner", matname=p["material_inner"]
        )
        diel = app.modeler.create_cylinder(
            cs_axis="Z", position=[0, 0, 0], radius=p["dielectric_radius"], height=50,
            name=f"{self.name}_diel", matname=p["material_diel"]
        )
        outer = app.modeler.create_cylinder(
            cs_axis="Z", position=[0, 0, 0], radius=p["outer_radius"], height=50,
            name=f"{self.name}_outer", matname=p["material_outer"]
        )
        # 進行布林運相減以完成挖空結構
        app.modeler.subtract(diel, inner, keep_originals=True)
        app.modeler.subtract(outer, diel, keep_originals=True)

# 編織屏蔽層建模實作 (關鍵：複雜參數化幾何)
class BraidedShieldParser(AnsysPyAEDTComponent):
    def build_geometry(self, app):
        p = self.params
        st.write(f"⚙️ 正在透過 PyAEDT 方程式線條計算編織層 {self.name} 的 3D 螺旋路徑...")

        # 模擬核心邏輯：在 PyAEDT 中使用 Equation-based Curve 建立螺旋線
        # 根據 num_carriers 與 braid_angle 迴圈建立單絲並 Sweep 沿路徑成形
        # 程式碼概念示意：
        # for i in range(p["num_carriers"]):
        #     eq_curve = app.modeler.create_equationbased_curve(x_t=..., y_t=..., z_t=...)
        #     strand = app.modeler.create_circle(position=..., radius=p["strand_diameter"]/2)
        #     app.modeler.sweep_along_path(strand, eq_curve)

        # 建立完成後將所有單絲群組或合併為一個物件，方便後續綁定 Boundary
        return True

# 註冊工廠
COMPONENT_MAP = {
    "Coaxial": CoaxialParser,
    "Braided_Shield": BraidedShieldParser
}

# ==================== 2. Streamlit 介面 ====================
st.set_page_config(page_title="ANSYS PyAnsys DSL Generator", layout="wide")
st.title("🎛️ 通用型傳輸線截面 ANSYS DSL 語法產生器")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 輸入傳輸線 YAML 配置")
    yaml_input = st.text_area("在此貼上您的 YAML 結構描述：", height=450, value="""ansys_project:
  name: "RF_Coax_Project"
  tool: "q3d"
  units: "mm"
  geometry_components:
    - name: "Main_Coax"
      type: "Coaxial"
      parameters:
        inner_radius: 0.5
        dielectric_radius: 1.6
        outer_radius: 1.8
        material_inner: "copper"
        material_diel: "teflon"
        material_outer: "copper"
      ports:
        - name: "Src_1"
          type: "Source"
          terminal_object: "Main_Coax_inner"
      boundaries:
        - name: "GND_1"
          type: "PerfectE"
          target_object: "Main_Coax_outer"
""")

with col2:
    st.subheader("2. 自動生成的 PyAnsys (.py) 腳本")

    if st.button("⚡ 解析 YAML 並生成 PyAnsys 程式碼"):
        try:
            parsed_yaml = yaml.safe_load(yaml_input)
            proj_config = parsed_yaml["ansys_project"]

            # 動態動態構建輸出的獨立 .py 腳本內容
            py_code = []
            py_code.append("from pyaedt import Q3d\n")
            py_code.append(f"q3d = Q3d(projectname='{proj_config['name']}', specified_version='2026.1')\n")
            py_code.append(f"q3d.modeler.model_units = '{proj_config['units']}'\n")

            # 遍歷元件渲染成腳本字串（此處為預覽輸出邏輯）
            for comp_data in proj_config["geometry_components"]:
                c_type = comp_data["type"]
                c_name = comp_data["name"]
                py_code.append(f"\n# --- 建立幾何元件與電磁邊界: {c_name} ({c_type}) ---")

                # 將工廠邏輯轉為純文字程式碼輸出供下載
                if c_type == "Coaxial":
                    p = comp_data["parameters"]
                    py_code.append(f"q3d.modeler.create_cylinder('Z', [0,0,0], {p['inner_radius']}, 50, name='{c_name}_inner', matname='{p['material_inner']}')")
                    py_code.append(f"q3d.modeler.create_cylinder('Z', [0,0,0], {p['dielectric_radius']}, 50, name='{c_name}_diel', matname='{p['material_diel']}')")
                    py_code.append(f"q3d.modeler.create_cylinder('Z', [0,0,0], {p['outer_radius']}, 50, name='{c_name}_outer', matname='{p['material_outer']}')")

                # 自動附加 Ports / Boundaries 腳本
                for port in comp_data.get("ports", []):
                    py_code.append(f"q3d.assign_source_to_sheet('{port['terminal_object']}', name='{port['name']}')")
                for bnd in comp_data.get("boundaries", []):
                    py_code.append(f"q3d.assign_perfecte('{bnd['target_object']}', name='{bnd['name']}')")

            final_script = "\n".join(py_code)
            st.code(final_script, language="python")

            st.download_button(
                label="💾 下載生成的 PyAnsys 腳本 (.py)",
                data=final_script,
                file_name=f"{proj_config['name']}_generated.py",
                mime="text/x-python"
            )

        except Exception as e:
            st.error(f"解析失敗，請檢查 YAML 格式或參數設定。錯誤訊息：{e}")
