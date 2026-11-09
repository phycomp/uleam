ansys_project:
  name: "Universal_Transmission_Line"
  design_type: "Q3D" # 支援 Q3D Extractor 或 HFSS
  units: "mm"

  # 1. 統一材料定義庫
  materials:
    - name: "Copper"
      conductivity: 58000000 # S/m
    - name: "FR4"
      permittivity: 4.4
      loss_tangent: 0.02
    - name: "Teflon"
      permittivity: 2.1
      loss_tangent: 0.0002

  # 2. 幾何元件清單（通用多型結構，依據 type 動態解析）
  geometry_components:

    # 範例 A：共面波導 (CPW) 結構
    - name: "CPW_Structure"
      type: "Coplanar_Waveguide"
      layer: 1
      parameters:
        trace_width: 0.5
        gap_width: 0.2
        ground_width: 2.0
        substrate_thickness: 1.6
        substrate_material: "FR4"
        trace_material: "Copper"

    # 範例 B：高頻同軸線 (Coaxial) 結構
    - name: "RF_Coax"
      type: "Coaxial"
      center_pos: [0, 0, 0]
      parameters:
        inner_conductor_radius: 0.45
        dielectric_radius: 1.5
        outer_shield_thickness: 0.1
        dielectric_material: "Teflon"
        conductor_material: "Copper"

    # 範例 C：編織屏蔽層 (Braided Shield) 結構
    - name: "Cable_Braided_Shield"
      type: "Braided_Shield"
      center_pos: [0, 0, 0]
      parameters:
        inner_radius: 1.6
        strand_diameter: 0.12     # 單根編織線直徑
        braid_angle_deg: 35        # 編織角度
        num_carriers: 16           # 載體數 (束數)
        strands_per_carrier: 4     # 每束的單絲數量
        material: "Copper"
