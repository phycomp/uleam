from streamlit import columns, markdown, plotly_chart, pyplot, set_page_config, sidebar, subheader, radio, slider, number_input, code
from plotly.graph_objects import Figure, Scatter
from matplotlib.pyplot import Rectangle, subplots
from numpy import abs, arange, pi, sqrt, zeros
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import cmath
from fontUtil2 import 中文字型
字=中文字型()
# tline_type, w_design, h_substrate, t_copper, dk, df
# for p in ['tline_type', 'w_design', 'h_substrate', 't_copper', 'dk', 'df']: print(f"{p}={p},")
def 渲染截面(tline_type, w_design, h_substrate, t_copper, dk, df):
  return f"""# 自動生成的傳輸線截面 DSL 配置
Structure("{tline_type.split()[0]}") {{
    Geometry {{
        Width     = {w_design} * um
        Height    = {h_substrate} * um
        Thickness = {t_copper} * um
        {"Spacing   = " + str(s_gap) + " * um" if "CPW" in tline_type else "# Single Conductor"}
    }}
    Material {{
        Dk = {dk}
        Df = {df}
    }}
}}
"""
# ==============================================================================
# 1. 網頁基本配置
# ==============================================================================
set_page_config(page_title="傳輸線截面 DSL 視覺化分析儀", layout="wide")
# ==============================================================================
# 2. 側邊欄：DSL 參數輸入區 (模擬 DSL 宣告)
# ==============================================================================
MENU, 表單=[], ['截面', '描述', '']		#, '錯綜複雜', '二十四節氣'
線類型=["Microstrip (微帶線)", "Stripline (帶狀線)", "CPW (共面波導)"]
for ndx, Menu in enumerate(表單): MENU.append(f'{ndx}{Menu}')
with sidebar:
  menu=radio('表單', MENU, horizontal=True, index=0)
  subheader("📁 1. 傳輸線截面 DSL 參數定義")

  # 選擇傳輸線類型
  tline_type = radio("選擇結構 (Placement Type)",  線類型, horizontal=True)

  # markdown("---")
  subheader("📐 幾何參數 (Geometric DSL)")
  w_design = slider("設計線寬 W (μm)", min_value=50, max_value=300, value=150, step=10)
  h_substrate = slider("介電層厚度 H (μm)", min_value=50, max_value=500, value=100, step=10)
  t_copper = slider("導體厚度 T (μm)", min_value=15, max_value=70, value=35, step=5)

  # 依據類型啟用特定參數
  s_gap = 100
  w_ground = 300
  if tline_type == "CPW (共面波導)":
      s_gap = slider("共面間距 S (μm)", min_value=20, max_value=200, value=50, step=10)
      w_ground = slider("旁路地寬 W_g (μm)", min_value=100, max_value=1000, value=400, step=50)

  # markdown("---")
  subheader("🧪 材料與損耗 (Material DSL)")
  dk = number_input("相對介電常數 (Dk)", min_value=1.0, max_value=10.0, value=4.3, step=0.1)
  df = number_input("損耗角正切 (Df)", min_value=0.0001, max_value=0.05, value=0.02, step=0.001, format="%.4f")

# ==============================================================================
# 3. 核心電磁計算引擎 (Python Backend)
# ==============================================================================
frequencies = arange(1.0e9, 21.0e9, 0.5e9) # 1 GHz 到 20 GHz 掃描
num_pts = len(frequencies)

# 依據幾何與材料特性，預估對應結構的近似基礎 R L G C（模擬場求解器行為）
if "Microstrip" in tline_type:
    L_base, C_base, R_coef = 3.1e-7, 1.2e-10 * (dk/4.3), 3.5
elif "Stripline" in tline_type:
    L_base, C_base, R_coef = 2.8e-7, 1.4e-10 * (dk/4.3), 4.2
else:  # CPW
    L_base, C_base, R_coef = 3.4e-7, 1.1e-10 * (dk/4.3), 5.1

# 依據線寬 W 與 厚度 H 進行阻抗修正微調
geometry_factor = sqrt(h_substrate / w_design)
L_base *= geometry_factor
C_base /= geometry_factor

z0_array = zeros(num_pts, dtype=complex)
loss_db_array = zeros(num_pts, dtype=float)

for i, freq in enumerate(frequencies):
    w = 2 * pi * freq
    w_scale = sqrt(freq / 1e9) # 高頻趨膚效應

    R = R_coef * w_scale * (35.0 / t_copper)
    L = L_base
    C = C_base
    G = w * C * df # 由 Df 推導的導納損耗

    Z = R + 1j * w * L
    Y = G + 1j * w * C

    z0_array[i] = cmath.sqrt(Z / Y)
    gamma = cmath.sqrt(Z * Y)
    loss_db_array[i] = gamma.real * 8.686 # Np/m -> dB/m

# ==============================================================================
# 4. 網頁佈局與可視化呈現
# ==============================================================================
col1, col2 = columns([1, 1])
from streamlit import empty, pyplot
狀態=empty()
with col1:
    subheader("🖼️ 2D 截面幾何預覽 (Cross-Section)")

    fig, ax = subplots(figsize=(6, 4))
    ax.set_facecolor("#f0f2f6")

    # 繪製介電層
    if "Stripline" in tline_type:
        ax.add_patch(Rectangle((-600, 0), 1200, h_substrate * 2 + t_copper, color="#dcd6be", label="Dielectric"))
        ax.add_patch(Rectangle((-600, -t_copper), 1200, t_copper, color="#b87333", label="GND Plane"))
        ax.add_patch(Rectangle((-600, h_substrate * 2 + t_copper), 1200, t_copper, color="#b87333"))
        ax.add_patch(Rectangle((-w_design/2, h_substrate), w_design, t_copper, color="#ff4b4b", label="Signal Trace"))
    elif "Microstrip" in tline_type:
        ax.add_patch(Rectangle((-600, 0), 1200, h_substrate, color="#dcd6be", label="Dielectric"))
        ax.add_patch(Rectangle((-600, -t_copper), 1200, t_copper, color="#b87333", label="GND Plane"))
        ax.add_patch(Rectangle((-w_design/2, h_substrate), w_design, t_copper, color="#ff4b4b", label="Signal Trace"))
    elif "CPW" in tline_type:
        ax.add_patch(Rectangle((-600, 0), 1200, h_substrate, color="#dcd6be", label="Dielectric"))
        # 繪製共面地與信號線
        trace_left = -w_design/2
        ax.add_patch(Rectangle((trace_left, h_substrate), w_design, t_copper, color="#ff4b4b", label="Signal Trace"))
        ax.add_patch(Rectangle((-600, h_substrate), 600 - w_design/2 - s_gap, t_copper, color="#b87333", label="GND Plane"))
        ax.add_patch(Rectangle((w_design/2 + s_gap, h_substrate), 600, t_copper, color="#b87333"))

    # 圖表美化
    ax.set_xlim(-500, 500)
    ax.set_ylim(-50, max(h_substrate*2.5, 300))
    ax.set_xlabel("Width (μm)")
    ax.set_ylabel("Height (μm)")
    ax.set_title(f"{tline_type} 幾何結構圖", fontsize=12, fontproperties=字)
    ax.legend(loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.6)

    pyplot(fig)

with col2:
    subheader("📊 關鍵電磁指標摘要 (@ 10 GHz)")
    idx_10g = (abs(frequencies - 10.0e9)).argmin()

    kpi_col1, kpi_col2 = columns(2)
    kpi_col1.metric(label="特徵阻抗 Z₀", value=f"{z0_array[idx_10g].real:.2f} Ω")
    kpi_col2.metric(label="高頻總損耗 (@10G)", value=f"{loss_db_array[idx_10g]:.2f} dB/m")

    markdown("### 📋 動態產生的 DSL 代碼描述")
    狀態.code(tline_type.split()[0])
    截面=渲染截面(tline_type, w_design, h_substrate, t_copper, dk, df)
    code(截面)  #dsl_template.format(tline_type=tline_type, w_design=w_design, h_substrate=h_substrate, t_copper=t_copper, dk=dk, df=df)
# {'tline_type':tline_type, 'w_design':w_design, 'h_substrate':h_substrate, 't_copper':t_copper, 'dk':dk, 'df':df}

# ==============================================================================
# 5. 全頻段特性響應圖表 (Plotly 互動圖表)
# ==============================================================================
# markdown("---")
subheader("📈 全頻段高頻特性掃描 (1 GHz - 20 GHz)")

plot_col1, plot_col2 = columns(2)

with plot_col1:
    fig_z0 = Figure()
    fig_z0.add_trace(Scatter(x=frequencies/1e9, y=z0_array.real, mode='lines', name='Z0 實部 (阻抗)', line=dict(color='#ff4b4b', width=3)))
    fig_z0.update_layout(title="特徵阻抗隨頻率變化 (Characteristic Impedance)", xaxis_title="Frequency (GHz)", yaxis_title="Impedance (Ohms)", template="plotly_white")
    plotly_chart(fig_z0, use_container_width=True)

with plot_col2:
    fig_loss = Figure()
    fig_loss.add_trace(Scatter(x=frequencies/1e9, y=loss_db_array, mode='lines', name='Loss (dB/m)', line=dict(color='#1f77b4', width=3, dash='dash')))
    fig_loss.update_layout(title="衰減損耗隨頻率變化 (Attenuation Loss)", xaxis_title="Frequency (GHz)", yaxis_title="Loss (dB/m)", template="plotly_white")
    plotly_chart(fig_loss, use_container_width=True)
with sidebar:
  # 本益比=slider("最高本益比(PE)", 0, 100, 25)
  # srch=text_input('搜尋', '')
  subheader("🎛️ 傳輸線截面 DSL 互動式視覺化分析儀")
  markdown("本工具提供**微帶線 (Microstrip)**、**帶狀線 (Stripline)** 及 **共面波導 (CPW)** 的幾何與高頻電磁特性即時計算。")
