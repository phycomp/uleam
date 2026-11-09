# ==============================================================================
# TRANSMISSION LINE CROSS-SECTION CONFIGURATION (通用傳輸線截面定義 DSL)
# ==============================================================================

Define_Project("Generic_TLine_Analysis")

# --- 1. 材料特性宣告 (Material Attributes) ---
Material("FR4_Core") {
    Dk = 4.3                             # 相對介電常數
    Df = 0.02                            # 損耗角正切
    Conductivity = 0.0                   # 介電質導電率
}

Material("Copper_Trace") {
    Conductivity = 5.8e7                 # 銅導體電導率 (S/m)
    Roughness_Model = "Huray"            # 高頻趨膚粗糙度模型
    Roughness_SR = 0.5                   # 表面粗糙度 (μm)
}

# --- 2. 堆疊與幾何參數 (Stackup & Geometric Parameters) ---
Parameter {
    H_substrate = 100.0 * um             # 介電層厚度
    T_copper    = 35.0  * um             # 導體厚度 (1 oz)
    W_design    = 150.0 * um             # 設計線寬
    Etch_Factor = 75.0  * deg            # 側邊側向蝕刻角度 (梯形截面)
    S_gap       = 200.0 * um             # 差動對邊界間距 (用於差動線定義)
}

# --- 3. 截面實體建構 (Cross-Section Entities) ---
Stackup {
    # 底部參考平面 (Ground Plane)
    Layer("GND_Bottom") {
        Type = "ReferencePlane"
        Material = "Copper_Trace"
        Thickness = T_copper
    }
    
    # 核心介電層
    Layer("Dielectric_Core") {
        Type = "Dielectric"
        Material = "FR4_Core"
        Thickness = H_substrate
    }
    
    # 信號走線層 (包含單端與差動通用描述)
    Layer("Signal_Top") {
        Type = "SignalLayer"
        Placement = "Microstrip"         # 可切換為 Microstrip 或 Stripline
        
        # 定義梯形傳輸線截面 (Top Width & Bottom Width 自動換算)
        Conductor("Trace_1") {
            Material = "Copper_Trace"
            Thickness = T_copper
            Width_Center = W_design
            Etch_Angle = Etch_Factor     # 考慮真實 PCB 製造的蝕刻效應
            X_Offset = 0.0               # 相對中心座標
        }
        
        # (選填) 若為差動對，解鎖第二條對稱線
        Conductor("Trace_2") {
            Material = "Copper_Trace"
            Thickness = T_copper
            Width_Center = W_design
            Etch_Angle = Etch_Factor
            X_Offset = W_design + S_gap  # 依據 Pitch / Spacing 擺放
        }
    }
}

# --- 4. 2D 場求解器網格剖分控制 (Solver Mesh Control) ---
Mesh_Setting {
    Mesh_Mode = "Adaptive"
    Max_Refinement_Passes = 10
    Mesh_Override("Trace_Edge") {        # 針對趨膚效應進行邊緣網格加密
        Target = ["Trace_1", "Trace_2"]
        Edge_Mesh_Size = 2.0 * um
    }
}
