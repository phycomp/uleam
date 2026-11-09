from streamlit import columns, error, markdown, metric, radio, subheader, success
from plotly.graph_objects import Scatter
# ==============================================================================
# 更新部分 2：PCIe 規範自動判定與極限線繪製 (置於網頁後半段的分析區)
# ==============================================================================
# st.markdown("---")
st.subheader("🛡️ 5. PCIe 通訊規範符合性自動判定 (Compliance Test)")

# 選擇要判定的規範版本
pcie_version = st.radio("選擇判定標準", ["PCIe Gen 5.0 (16 GHz Nyquist)", "PCIe Gen 6.0 (32 GHz Nyquist)"], horizontal=True)

# 依據標準設定奈奎斯特頻率與串擾容許極限 (dB)
if "Gen 5.0" in pcie_version:
    nyquist_f = 16.0  # GHz
    crosstalk_limit = -32.0  # dB Max 容許值
else:
    nyquist_f = 32.0  # GHz
    crosstalk_limit = -28.0  # dB Max 容許值

# 計算目標奈奎斯特點上的實際 Victim 最大串擾
R_comp, L_comp, G_comp, C_comp = build_n_channel_matrices(num_lines, w_nominal, s_nominal, h_nominal, t_nominal, dk, df, nyquist_f*1e9)
all_xtalks = solve_mtl_crosstalk(R_comp, L_comp, G_comp, C_comp, nyquist_f*1e9, line_len, aggressor_idx)

# 排除 Aggressor 本身，找出最大的 Victim 串擾值
victim_xtalks = [all_xtalks[i] for i in range(num_lines) if i != aggressor_idx]
max_victim_xtalk = max(victim_xtalks) if victim_xtalks else -100.0

# 顯示規範判定結果 KPI
comp_col1, comp_col2, comp_col3 = st.columns(3)
with comp_col1:
    st.metric(label="測試奈奎斯特頻率", value=f"{nyquist_f} GHz")
with comp_col2:
    st.metric(label="規範串擾上限", value=f"{crosstalk_limit} dB")
with comp_col3:
    if max_victim_xtalk <= crosstalk_limit:
        st.success(f"🟢 PASS (最大串擾: {max_victim_xtalk:.2f} dB)")
    else:
        st.error(f"🔴 FAIL (最大串擾: {max_victim_xtalk:.2f} dB，超出規範！)")

# 在原本的 Plotly 圖表中，同步動態疊加 PCIe 規範限線 (Mask)
# 修改原圖表代碼，在顯示前加上以下這段：
fig_plotly.add_trace(go.Scatter(
    x=[f_start, f_stop], 
    y=[crosstalk_limit, crosstalk_limit], 
    name=f"{pcie_version} 限線", 
    line=dict(color='black', width=2, dash='dot')
))
