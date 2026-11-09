# ------------------------------------------------------------------------------
# ANSYS AEDT (2D Extractor) AUTOMATION SCRIPT - FULL TRANSMISSION LINE SUITE
# ------------------------------------------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansys.AnsoftSgEnv.AnsoftSgCurrentSrcEngine")
oAnsoftApp.SetActiveProject("CrossSection_Automation")
oProject = oAnsoftApp.GetActiveProject()
oDesign = oProject.InsertDesign("2D Extractor", "TLine_Suite", "OpenMatrix_Standard")
oEditor = oDesign.SetActiveEditor("2DModeler")

# --- 1. 定義通用參數化幾何 (DSL Variables) ---
def setup_variables():
    variables = {
        "H_sub": "100um",       # 介電層厚度
        "T_copper": "35um",     # 銅厚 (1 oz)
        "W_trace": "150um",     # 線寬
        "S_gap": "200um",       # 差動/CPW 間距
        "W_ground": "500um"     # CPW 旁路地寬
    }
    for var, val in variables.items():
        oDesign.ChangeProperty(["NAME:AllTabs", ["NAME:LocalVariableTab", ["NAME:PropServers", "LocalVariables"], ["NAME:NewProps", ["NAME:" + var, "Value:=", val]]]])

# --- 2. 封裝傳輸線截面建立函數 ---
def create_rectangle(name, x, y, width, height, material="copper"):
    oEditor.CreateRectangle(
        ["NAME:RectangleParameters", "CoordinateSystem:=", "Global", "XStart:=", x, "YStart:=", y, "ZStart:=", "0mm", "Width:=", width, "Height:=", height, "WhichAxis:=", "Z"],
        ["NAME:Attributes", "Name:=", name, "Flags:=", "", "Color:=", "(132 132 193)", "MaterialName:=", material, "GridInterval:=", "0mm"]
    )

def build_transmission_lines():
    setup_variables()
    
    # === TYPE A: Microstrip (微帶線) ===
    create_rectangle("GND_Microstrip", "-500um", "0mm", "2000um", "T_copper", "copper")
    create_rectangle("Sub_Microstrip", "-500um", "T_copper", "2000um", "H_sub", "FR4_epoxy")
    create_rectangle("Trace_Microstrip", "0mm", "T_copper + H_sub", "W_trace", "T_copper", "copper")
    
    # === TYPE B: Stripline (帶狀線) ===
    create_rectangle("GND_Strip_Bot", "-500um", "500um", "2000um", "T_copper", "copper")
    create_rectangle("Sub_Strip_Bot", "-500um", "500um + T_copper", "2000um", "H_sub", "FR4_epoxy")
    create_rectangle("Trace_Stripline", "0mm", "500um + T_copper + H_sub", "W_trace", "T_copper", "copper")
    create_rectangle("Sub_Strip_Top", "-500um", "500um + T_copper + H_sub + T_copper", "2000um", "H_sub", "FR4_epoxy")
    create_rectangle("GND_Strip_Top", "-500um", "500um + T_copper*2 + H_sub*2", "2000um", "T_copper", "copper")

    # === TYPE C: Coplanar Waveguide (CPW 共面波導) ===
    base_y = "1500um"
    create_rectangle("Sub_CPW", "-500um", base_y, "2000um", "H_sub", "FR4_epoxy")
    create_rectangle("GND_CPW_Left", "-500um", base_y + " + H_sub", "W_ground", "T_copper", "copper")
    create_rectangle("Trace_CPW", "-500um + W_ground + S_gap", base_y + " + H_sub", "W_trace", "T_copper", "copper")
    create_rectangle("GND_CPW_Right", "-500um + W_ground + S_gap + W_trace + S_gap", base_y + " + H_sub", "W_ground", "T_copper", "copper")

# --- 3. 執行指派與分析 ---
build_transmission_lines()
oDesign.AnalyzeAll()

# --- 4. 自動化匯出：將求解矩陣匯出為 OpenMatrix 相容的常規文字檔 ---
oModule = oDesign.GetModule("Solutions")
oModule.ExportMatrixData(
    "C:\\Ansys_Automation\\Output\\tline_matrix_dump.txt", 
    "Matrix1", "Original", "Frequency", "ALL", "Data", "RealImag", "Tab"
)
print("AEDT 模擬完成，RLGC 網格矩陣資料已成功匯出。")
