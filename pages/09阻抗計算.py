from streamlit import columns, components, error, metric, set_page_config, sidebar, subheader, success, title
import streamlit as st
from 計算 import calc_microstrip_qubit

# --- 2. Streamlit 介面佈局 ---
st.set_page_config(layout="wide")
st.title("🎛 量子位元讀取傳輸線 (4-12 GHz) 智能計算平台")

# 側邊欄：參數輸入與本地材料庫
st.sidebar.header("⚡ 物理結構參數")
material = st.sidebar.selectbox("選擇微波基材 (MVP 材料庫)", ["Rogers RO4003C", "PTFE", "High-Res Silicon"])
freq = st.sidebar.slider("工作頻率 (GHz)", 4.0, 12.0, 8.0, step=0.5)

# 映射材料 Dk
er_map = {"Rogers RO4003C": 3.38, "PTFE": 2.10, "High-Res Silicon": 11.70}
Er = er_map[material]

# 核心拖曳滑桿 (響應時間 < 50ms)
W = st.sidebar.slider("線寬 W (mils)", 2.0, 30.0, 10.0, step=0.1)
H = st.sidebar.slider("介質厚度 H (mils)", 5.0, 50.0, 20.0, step=0.5)
T = 1.4  # 固定 1oz 銅厚

# --- 3. 呼叫引擎計算 ---
Z0, alpha_d = calc_microstrip_qubit(W, H, T, Er, freq)

# --- 4. 疊構畫布渲染 (使用動態 SVG 嵌入 Streamlit) ---
# 計算畫布中線寬與厚度的相對比例
svg_w = W * 10
svg_h = H * 5

svg_code = f"""
<svg width="100%" height="200" viewBox="0 0 600 200" xmlns="http://w3.org">
    <!-- 背景/空氣層 -->
    <rect width="600" height="200" fill="#1E1E1E" />
    
    <!-- 介質層 (Dielectric Layer) -->
    <rect x="50" y="100" width="500" height="{max(30, svg_h)}" fill="#2D5A27" opacity="0.8" rx="5"/>
    <text x="60" y="{100 + max(20, svg_h/2)}" fill="#FFFFFF" font-family="sans-serif" font-size="12">{material} (Dk={Er})</text>
    
    <!-- 導體線寬 (Microstrip Signal Trace) -->
    <rect x="{300 - svg_w/2}" y="{100 - 10}" width="{max(20, svg_w)}" height="10" fill="#E5A93C" rx="2"/>
    <text x="300" y="80" fill="#E5A93C" font-family="sans-serif" font-size="14" text-anchor="middle" font-weight="bold">W = {W} mils</text>
    
    <!-- 下參考地平面 (GND Plane) -->
    <rect x="50" y="{100 + max(30, svg_h)}" width="500" height="8" fill="#A0A0A0" />
    <text x="60" y="{100 + max(30, svg_h) + 25}" fill="#A0A0A0" font-family="sans-serif" font-size="12">GND Plane</text>
</svg>
"""

# 畫布與數據並排顯示
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📐 傳輸線截面動態畫布 (SVG 實時渲染)")
    st.components.v1.html(svg_code, height=220)

with col2:
    st.subheader("📊 物理仿真結果")
    st.metric(label="🎯 特性阻抗 (Characteristic Impedance)", value=f"{Z0} Ω")
    
    # 量子位元最在乎的損耗指標
    st.metric(label="📉 估算介質損耗 (Dielectric Loss)", value=f"{alpha_d} dB/cm")
    
    # 阻抗匹配警告機制
    if abs(Z0 - 50.0) > 5.0:
        st.error(f"❌ 阻抗偏離 50Ω 達到 {round(abs(Z0-50),1)}Ω！在高頻下會引發嚴重反射，影響量子比特讀取。")
    else:
        st.success("✅ 阻抗完美匹配 50Ω ($\pm$5Ω 內)，適合 4-12 GHz 訊號傳輸。")
