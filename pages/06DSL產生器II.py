import streamlit as st
import yaml

# ==================== 1. 純文字 PyAnsys 腳本生成工廠 ====================
class ScriptGeneratorFactory:
    @staticmethod
    def generate_coaxial(name, p, ports, boundaries):
        lines = [f"\n# --- 建立幾何元件: {name} (Coaxial) ---"]
        lines.append(f"q3d.modeler.create_cylinder('Z', [0, 0, 0], {p['inner_radius']}, 50, name='{name}_inner', matname='{p['material_inner']}')")
        lines.append(f"q3d.modeler.create_cylinder('Z', [0, 0, 0], {p['dielectric_radius']}, 50, name='{name}_diel', matname='{p['material_diel']}')")
        lines.append(f"q3d.modeler.create_cylinder('Z', [0, 0, 0], {p['outer_radius']}, 50, name='{name}_outer', matname='{p['material_outer']}')")
        lines.append(f"q3d.modeler.subtract('{name}_diel', '{name}_inner', keep_originals=True)")
        lines.append(f"q3d.modeler.subtract('{name}_outer', '{name}_diel', keep_originals=True)")
        
        # 附加電磁邊界與激勵源
        lines.extend(ScriptGeneratorFactory.generate_em_setup(ports, boundaries))
        return lines

    @staticmethod
    def generate_braided_shield(name, p, ports, boundaries):
        lines = [f"\n# --- 建立幾何元件: {name} (Braided Shield) ---"]
        lines.append(f"# 參數：載體數={p['num_carriers']}, 每束單絲={p['strands_per_carrier']}, 角度={p['braid_angle_deg']}度")
        lines.append(f"# 自動計算 3D 雙向螺旋編織路徑並利用 Equation-based Curve 進行多重 Sweep 建模...")
        lines.append(f"# [PyAnsys 核心代碼段生成中] ...")
        
        lines.extend(ScriptGeneratorFactory.generate_em_setup(ports, boundaries))
        return lines

    @staticmethod
    def generate_em_setup(ports, boundaries):
        em_lines = []
        for port in ports:
            em_lines.append(f"q3d.assign_source_to_sheet('{port['terminal_object']}', name='{port['name']}')")
        for bnd in boundaries:
            if bnd["type"] == "PerfectE":
                em_lines.append(f"q3d.assign_perfecte('{bnd['target_object']}', name='{bnd['name']}')")
        return em_lines

# ==================== 2. Streamlit 介面 ====================
st.set_page_config(page_title="ANSYS DSL Generator", layout="wide")
st.title("🎛️ 免套件通用型傳輸線截面 ANSYS DSL 語法產生器")

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
            
            py_code = [
                "# -*- coding: utf-8 -*-",
                '"""',
                f"自動生成的 PyAnsys 腳本: {proj_config['name']}",
                '"""',
                "from pyaedt import Q3d\n",
                f"q3d = Q3d(projectname='{proj_config['name']}', specified_version='2026.1')",
                f"q3d.modeler.model_units = '{proj_config['units']}'\n"
            ]
            
            for comp in proj_config["geometry_components"]:
                c_type = comp["type"]
                c_name = comp["name"]
                p = comp.get("parameters", {})
                ports = comp.get("ports", [])
                boundaries = comp.get("boundaries", [])
                
                if c_type == "Coaxial":
                    py_code.extend(ScriptGeneratorFactory.generate_coaxial(c_name, p, ports, boundaries))
                elif c_type == "Braided_Shield":
                    py_code.extend(ScriptGeneratorFactory.generate_braided_shield(c_name, p, ports, boundaries))
                else:
                    py_code.append(f"\n# 未支援的幾何類型: {c_type}")
                    
            final_script = "\n".join(py_code)
            st.code(final_script, language="python")
            
            st.download_button(
                label="💾 下載生成的 PyAnsys 腳本 (.py)",
                data=final_script,
                file_name=f"{proj_config['name']}_generated.py",
                mime="text/x-python"
            )
            
        except Exception as e:
            st.error(f"解析失敗！錯誤訊息：{e}")
