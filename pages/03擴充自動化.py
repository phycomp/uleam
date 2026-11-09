from streamlit import cache_data, columns, dataframe, markdown, metric, plotly_chart, pyplot, set_page_config, sidebar, subheader, radio, slider, number_input
from plotly.graph_objects import Box, Figure, Histogram
from matplotlib.pyplot import Rectangle, subplots
from numpy import array, diag, dot, linalg, log10, pi, random, sqrt, sum
from numpy.random import normal
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.linalg import expm
import cmath

# ==============================================================================
# 0. 網頁基本配置
# ==============================================================================
set_page_config(page_title="多導體傳輸線高頻自動化分析儀", layout="wide")
subheader("🚀 多導體傳輸線截面自動化分析與公差預測儀")
markdown("本系統整合 **1. 幾何 DSL 描述**、**2. 多導體矩陣導出**、**3. 電磁計算**、**4. 蒙地卡羅良率掃描** 與 **5. 近/遠端串擾分析**。")
MENU, 表單=[], ['截面', '阻抗', '']		#, '錯綜複雜', '二十四節氣'
for ndx, Menu in enumerate(表單): MENU.append(f'{ndx}{Menu}')
with sidebar:
  menu=radio('表單', MENU, horizontal=True, index=0)
# ==============================================================================
# 1. 側邊欄：DSL 參數輸入區 (隨機製造公差配置)
# ==============================================================================
  subheader("📁 傳輸線 DSL 與製造公差配置")
  tline_type = radio("結構類型 (Type)", ["Microstrip (微帶線)", "Stripline (帶狀線)"], horizontal=True)

  subheader("📐 幾何名義值 (Nominal DSL)")
  w_nominal = slider("線寬 W (μm)", 50, 300, 150)
  h_nominal = slider("介電厚度 H (μm)", 50, 500, 100)
  t_nominal = slider("導體厚度 T (μm)", 15, 70, 35)
  s_nominal = slider("線間距 S (μm)", 50, 400, 150)

  subheader("🎲 製造公差波動 (Monte Carlo Tolerance)")
  w_sigma = slider("線寬標準差 σ_W (μm)", 0.0, 10.0, 3.0, step=0.5)
  h_sigma = slider("厚度標準差 σ_H (μm)", 0.0, 10.0, 2.5, step=0.5)
  dk_sigma = slider("介電常數標準差 σ_Dk", 0.0, 0.2, 0.05, step=0.01)

  subheader("⚡ 系統模擬條件 (Simulation DSL)")
  freq_target = number_input("目標分析頻率 (GHz)", 1.0, 30.0, 10.0, step=1.0)
  line_len = number_input("傳輸線實際長度 (米)", 0.01, 1.0, 0.1, step=0.05)
  mc_samples = radio("蒙地卡羅抽樣次數", [100, 500, 1000], index=1, horizontal=True)

# ==============================================================================
# 2. 核心電磁場求解與矩陣導出引擎 (Multi-Conductor Matrix Engine)
# ==============================================================================
def derive_rlgc_matrices(w, h, t, s, dk, df, freq):
    """
    動態導出 2-Conductor (差動/鄰近雙線) 系統的 2x2 RLGC 矩陣 (2D Field Solver 核心模擬)
    """
    w_m, h_m, t_m, s_m = w*1e-6, h*1e-6, t*1e-6, s*1e-6
    omega = 2 * pi * freq
    
    # 互容與自容矩陣導出 (考慮邊界場微擾)
    c_self = 8.854e-12 * dk * (w_m / h_m + 1.2)
    c_mutual = 8.854e-12 * dk * (0.5 / (s_m / h_m + 0.1))
    C = array([[c_self + c_mutual, -c_mutual], 
                  [-c_mutual, c_self + c_mutual]])
    
    # 互感與自感矩陣導出 (基於光速不變性與空間微擾)
    L = 1.256e-6 * 8.854e-12 * 1.0 / C
    # 修正非對角線對稱度
    L[0,1] = L[1,0] = L[0,0] * (0.2 / (s_m/h_m + 0.5))
    
    # 高頻趨膚效應電阻矩陣 R 與 介電損耗導納矩陣 G
    r_skin = 1.0 / (5.8e7 * t_m * w_m) * sqrt(freq / 1e9)
    R = array([[r_skin, 0.0], [0.0, r_skin]])
    G = omega * C * df
    
    return R, L, G, C

def analyze_crosstalk(R, L, G, C, freq, length):
    """
    基於多導體傳輸線電報方程 (Telegrapher's Equations Matrix Exponent) 計算 NEXT / FEXT
    """
    omega = 2 * pi * freq
    Z_mat = R + 1j * omega * L
    Y_mat = G + 1j * omega * C
    
    # 系統矩陣
    YZ = dot(Y_mat, Z_mat)
    # 核心矩陣指數解算電壓傳播常數
    prop_mat = expm(-sqrt_matrix(YZ) * length)
    
    # 假設主動線輸入 1V 電壓，靜態線近端與遠端的耦合分析
    next_xtalk = 20 * log10(max(1e-6, abs(prop_mat[0, 1] * 0.3)))  # 近端串擾估算
    fext_xtalk = 20 * log10(max(1e-6, abs(prop_mat[1, 0])))       # 遠端串擾矩陣值
    return next_xtalk, fext_xtalk

def sqrt_matrix(mat):
    """矩陣開平方根輔助函式"""
    evals, evecs = linalg.eig(mat)
    return dot(evecs, dot(diag(sqrt(evals)), linalg.inv(evecs)))

# 計算名義值
R_n, L_n, G_n, C_n = derive_rlgc_matrices(w_nominal, h_nominal, t_nominal, s_nominal, 4.3, 0.02, freq_target*1e9)
Z0_nominal = sqrt(L_n[0,0]/C_n[0,0])

# ==============================================================================
# 3. 蒙地卡羅良率掃描引擎 (Monte Carlo Engine)
# ==============================================================================
@cache_data
def run_monte_carlo(w, h, t, s, w_s, h_s, dk_s, freq, samples):
    z0_list = []
    next_list = []
    fext_list = []
    
    # 產生高斯隨機製造誤差
    w_samples = normal(w, w_s, samples)
    h_samples = normal(h, h_s, samples)
    dk_samples = normal(4.3, dk_s, samples)
    
    for i in range(samples):
        R, L, G, C = derive_rlgc_matrices(w_samples[i], h_samples[i], t, s, dk_samples[i], 0.02, freq)
        z0 = sqrt(L[0,0]/C[0,0])
        nxt, fxt = analyze_crosstalk(R, L, G, C, freq, line_len)
        z0_list.append(z0)
        next_list.append(nxt)
        fext_list.append(fxt)
        
    return array(z0_list), array(next_list), array(fext_list)

z0_s, next_s, fext_s = run_monte_carlo(w_nominal, h_nominal, t_nominal, s_nominal, w_sigma, h_sigma, dk_sigma, freq_target*1e9, mc_samples)

# 計算阻抗良率 (標準常規：50Ω ± 10% 為合格基準，即 45Ω ~ 55Ω)
yield_rate = sum((z0_s >= 45) & (z0_s <= 55)) / mc_samples * 100

# ==============================================================================
# 4. 網頁佈局與數據視覺化呈現
# ==============================================================================
col1, col2 = columns([1, 1])

with col1:
    subheader("🖼️ 1. 雙導體截面幾何 DSL 生成器")
    fig, ax = subplots(figsize=(6, 3))
    ax.set_facecolor("#f8f9fa")
    
    # 繪製多導體幾何結構
    ax.add_patch(Rectangle((-500, 0), 1000, h_nominal, color="#dcd6be", label="Substrate"))
    ax.add_patch(Rectangle((-500, -t_nominal), 1000, t_nominal, color="#b87333", label="GND"))
    # 主動線與被動線
    ax.add_patch(Rectangle((-w_nominal - s_nominal/2, h_nominal), w_nominal, t_nominal, color="#ff4b4b", label="Trace 1 (Aggressor)"))
    ax.add_patch(Rectangle((s_nominal/2, h_nominal), w_nominal, t_nominal, color="#1f77b4", label="Trace 2 (Victim)"))
    
    ax.set_xlim(-400, 400)
    ax.set_ylim(-50, h_nominal + 80)
    ax.set_xlabel("Width (μm)")
    ax.set_ylabel("Height (μm)")
    ax.legend(loc="upper right", fontsize='small')
    pyplot(fig)
    
    subheader("📋 2. 導出的多導體 RLGC 網格矩陣 (@ 目標頻率)")
    markdown(f"**單位長度電感矩陣 L (nH/m):**")
    dataframe(L_n * 1e9)
    markdown(f"**單位長度電容矩陣 C (pF/m):**")
    dataframe(C_n * 1e12)

with col2:
    subheader("🎲 4. 蒙地卡羅阻抗良率預測 (良率控制)")
    metric(label=f"阻抗控制良率良率基準 (目標 50Ω ±10%)", value=f"{yield_rate:.1f} %")
    
    # 阻抗分佈直方圖
    fig_hist = Figure()
    fig_hist.add_trace(Histogram(x=z0_s, name='阻抗分佈', marker_color='#ff4b4b', opacity=0.75))
    fig_hist.add_vline(x=45, line_dash="dash", line_color="red", annotation_text="下限 45Ω")
    fig_hist.add_vline(x=55, line_dash="dash", line_color="red", annotation_text="上限 55Ω")
    fig_hist.update_layout(title="蒙地卡羅隨機製造抽樣阻抗分佈圖", xaxis_title="Impedance (Ohms)", yaxis_title="Count", template="plotly_white", height=320)
    plotly_chart(fig_hist, use_container_width=True)

# ==============================================================================
# 5. 串擾分析區 (NEXT / FEXT Crosstalk Matrix Analysis)
# ==============================================================================
# markdown("---")
subheader("⚡ 5. 鄰近多導體串擾（Crosstalk）與矩陣分析")

xtalk_col1, xtalk_col2, xtalk_col3 = columns(3)

with xtalk_col1:
    nominal_next, nominal_fext = analyze_crosstalk(R_n, L_n, G_n, C_n, freq_target*1e9, line_len)
    markdown("### 名義設計指標")
    metric(label="單端特徵阻抗 Z₀", value=f"{Z0_nominal:.2f} Ω")
    metric(label="近端串擾 NEXT", value=f"{nominal_next:.2f} dB")
    metric(label="遠端串擾 FEXT", value=f"{nominal_fext:.2f} dB")

with xtalk_col2:
    # 串擾隨波動分佈
    fig_xtalk = Figure()
    fig_xtalk.add_trace(Box(y=next_s, name="NEXT (近端)", marker_color="#ab63fa"))
    fig_xtalk.add_trace(Box(y=fext_s, name="FEXT (遠端)", marker_color="#00cc96"))
    fig_xtalk.update_layout(title="公差引起的串擾波動範圍 (dB)", yaxis_title="Crosstalk (dB)", template="plotly_white", height=320)
    plotly_chart(fig_xtalk, use_container_width=True)

with xtalk_col3:
    # 說明面板
    markdown("""
    ### 💡 多導體分析備忘錄
    1. **互感與互容矩陣**：自導體的邊緣場（Fringing Field）是引起多導體串擾的主要物理成因，當線距 `S` 縮小時，`L[0,1]` 與 `C[0,1]` 將顯著增大。
    2. **NEXT (近端串擾)**：主要受電磁耦合總量影響，在長度達到飽和長度後不再隨長度增加。
    3. **FEXT (遠端串擾)**：受微帶線不均勻介電質環境（空氣與 FR4）影響，高頻下損耗會隨傳輸線長度 `Line Length` 呈現線性惡化。
    """)
