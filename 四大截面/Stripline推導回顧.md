# ============================================================
# 1. Stripline 推導回顧 + 完整文件
# ============================================================

stripline_doc = """
═══════════════════════════════════════════════════════════════
1. STRIPLINE（帶狀線）
═══════════════════════════════════════════════════════════════

【物理模型】

    GND  y = +b/2
    ─────────────────────────────
         |  Dielectric εᵣ  |
         |                   |
    █████|████ Signal w ████|█████  y = 0
         |                   |
         |  Dielectric εᵣ  |
    ─────────────────────────────
    GND  y = -b/2

【關鍵特徵】
• 純 TEM 模 — 均勻介質填充
• ε_eff = εᵣ（精確成立）
• 雙接地平面對稱結構

【保角映射精確解】

Z₀·√εᵣ = 30π · K(k')/K(k)

其中 k = sech(πw / 2b),  k' = √(1-k²)

【工程閉式公式（Wadell / IPC-2141A）】

窄帶狀線（w/b ≤ 0.35）:
    Z₀ = (60/√εᵣ) · ln(8b/πw)

寬帶狀線（w/b ≥ 0.35）:
    Z₀ = (94.15/√εᵣ) / (w/b + 0.441)

【厚度修正】

w_eff = w - Δw

w/b ≤ 0.35:  Δw = (t/π) · ln(2b/t)
w/b > 0.35:  Δw = (t/π) · ln(2πw/t)
"""
print(stripline_doc)

# Python 實作
class StriplineAnalytical:
    """Stripline 解析模型"""
    
    @classmethod
    def characteristic_impedance(cls, w_over_b, eps_r):
        if w_over_b <= 0.35:
            return (60 / np.sqrt(eps_r)) * np.log(8 / (np.pi * w_over_b))
        else:
            return (94.15 / np.sqrt(eps_r)) / (w_over_b + 0.441)
    
    @classmethod
    def thickness_correction(cls, w, b, t):
        wb = w / b
        if wb <= 0.35:
            dw = (t / np.pi) * np.log(2 * b / t)
        else:
            dw = (t / np.pi) * np.log(2 * np.pi * w / t)
        return w - dw
    
    @classmethod
    def analyze(cls, w, b, t=0, eps_r=4.2):
        w_eff = cls.thickness_correction(w, b, t) if t > 0 else w
        wb = w / b
        Z0 = cls.characteristic_impedance(wb, eps_r)
        wb_eff = w_eff / b
        Z0_corr = cls.characteristic_impedance(wb_eff, eps_r)
        return {'w_over_b': wb, 'eps_eff': eps_r, 'Z0': Z0, 
                'Z0_corrected': Z0_corr, 'delta_w': w - w_eff if t > 0 else 0}

print("✓ Stripline 模型已載入")
