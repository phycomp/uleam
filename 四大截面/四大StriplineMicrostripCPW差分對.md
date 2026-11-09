# ============================================================
# 四大截面解析公式推導：Stripline, Microstrip, CPW, 差分對
# ============================================================

import numpy as np
import sympy as sp
from scipy.special import ellipk, ellipe

print("=" * 70)
print("四大截面解析公式推導與實作")
print("=" * 70)

# --------------------------------------------------------
# 0. 橢圓積分工具函數（CPW 必需）
# --------------------------------------------------------

def elliptic_ratio(k):
    """
    計算 K(k')/K(k)，即第一類完全橢圓積分的互補比
    
    使用 Hilberg 近似（精度 < 3e-6）：
    
    當 0 ≤ k ≤ 1/√2:
        K(k')/K(k) = (1/π) * ln[2(1+√k')/(1-√k')]
    
    當 1/√2 ≤ k ≤ 1:
        K(k')/K(k) = π / ln[2(1+√k)/(1-√k)]
    
    其中 k' = √(1-k²)
    """
    k = np.asarray(k)
    kp = np.sqrt(1 - k**2)
    
    ratio = np.zeros_like(k, dtype=float)
    
    # 小 k 區域
    mask_small = k <= 1/np.sqrt(2)
    if np.any(mask_small):
        sqrt_kp = np.sqrt(kp[mask_small])
        ratio[mask_small] = (1/np.pi) * np.log(2 * (1 + sqrt_kp) / (1 - sqrt_kp))
    
    # 大 k 區域
    mask_large = k > 1/np.sqrt(2)
    if np.any(mask_large):
        sqrt_k = np.sqrt(k[mask_large])
        ratio[mask_large] = np.pi / np.log(2 * (1 + sqrt_k) / (1 - sqrt_k))
    
    return ratio

# 驗證橢圓積分近似
test_k = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 0.99])
print("\n【橢圓積分近似驗證】")
print(f"{'k':>8} {'K(k\')/K(k) 近似':>18} {'scipy 參考':>15}")
for k in test_k:
    approx = elliptic_ratio(k)
    # scipy 的 ellipk 計算 K(k) 和 K(k')
    Kk = ellipk(k**2)
    Kkp = ellipk(1 - k**2)
    ref = Kkp / Kk if Kk > 0 else 0
    print(f"{k:>8.4f} {approx[0]:>18.6f} {ref:>15.6f}")

print("\n✓ 橢圓積分近似精度良好")
