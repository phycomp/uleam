ansys_project:
  name: "High_Freq_Cable_Design"
  tool: "q3d" # 可選 hfss, q3d, maxwell
  units: "mm"

  geometry_components:
    # 範例 A：高頻同軸線 (Coaxial)
    - name: "RF_Coax_Main"
      type: "Coaxial"
      parameters:
        inner_radius: 0.5
        dielectric_radius: 1.6
        outer_radius: 1.8
        material_inner: "copper"
        material_diel: "teflon"
        material_outer: "copper"

      # 同步生成 Ports (激勵源)
      ports:
        - name: "Port_In"
          type: "WavePort" # 或 Source/Sink (Q3D)
          terminal_object: "RF_Coax_Main_inner" # 指定綁定的幾何名稱
          reference_object: "RF_Coax_Main_outer"
          position_z: 0.0

      # 同步生成 Boundaries (邊界條件)
      boundaries:
        - name: "PerfectE_Outer"
          type: "PerfectE"
          target_object: "RF_Coax_Main_outer"

    # 範例 B：編織屏蔽層 (Braided Shield)
    - name: "Shield_Layer_01"
      type: "Braided_Shield"
      parameters:
        inner_radius: 1.8
        strand_diameter: 0.1
        braid_angle_deg: 40
        num_carriers: 24
        strands_per_carrier: 5
        material: "copper"

      # 編織層通常作為整體參考地 (Ground)
      boundaries:
        - name: "Shield_GND"
          type: "PerfectE"
          target_object: "Shield_Layer_01"
