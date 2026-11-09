from numpy import any, asarray, clip, exp, isinf, log, pi, sinh, sqrt, tanh, zeros_like
## 5. 統一 Python 實作

# import numpy as np

# 橢圓積分工具
def elliptic_ratio(k):
    k = np.asarray(k)
    kp = np.sqrt(1 - k**2)
    ratio = np.zeros_like(k, dtype=float)
    mask_small = k <= 1/np.sqrt(2)
    if np.any(mask_small):
        sqrt_kp = np.sqrt(kp[mask_small])
        ratio[mask_small] = (1/np.pi) * np.log(2*(1+sqrt_kp)/(1-sqrt_kp))
    mask_large = k > 1/np.sqrt(2)
    if np.any(mask_large):
        sqrt_k = np.sqrt(k[mask_large])
        ratio[mask_large] = np.pi / np.log(2*(1+sqrt_k)/(1-sqrt_k))
    return ratio

# Stripline
class StriplineAnalytical:
    @classmethod
    def analyze(cls, w, b, t=0, eps_r=4.2):
        wb = w / b
        if wb <= 0.35:
            Z0 = (60 / np.sqrt(eps_r)) * np.log(8 / (np.pi * wb))
        else:
            Z0 = (94.15 / np.sqrt(eps_r)) / (wb + 0.441)
        return {'Z0': Z0, 'eps_eff': eps_r}

# Microstrip
class MicrostripAnalytical:
    ETA_0 = 120 * np.pi
    @classmethod
    def analyze(cls, w, h, t=0, eps_r=4.2):
        wh = w / h
        a, b = (eps_r + 1)/2, (eps_r - 1)/2
        F = (1 + 12/wh)**(-0.5) + (0.04*(1-wh)**2 if wh <= 1 else 0)
        eps_eff = a + b * F
        if wh <= 1:
            Z0 = (cls.ETA_0/(2*np.pi*np.sqrt(eps_eff))) * np.log(8/wh + wh/4)
        else:
            Z0 = cls.ETA_0 / (np.sqrt(eps_eff)*(wh + 1.393 + 0.667*np.log(wh+1.444)))
        return {'Z0': Z0, 'eps_eff': eps_eff}

# CPW
class CPWAnalytical:
    @classmethod
    def analyze(cls, s, w, h, t=0, eps_r=4.2):
        d = s + 2*w
        k = s / d
        if np.isinf(h) or h > 10*d:
            q = 0.5
        else:
            arg_s = np.clip(np.pi*s/(4*h), -700, 700)
            arg_d = np.clip(np.pi*d/(4*h), -700, 700)
            k1 = np.clip(np.sinh(arg_s)/np.sinh(arg_d), 0, 1)
            ratio_k = elliptic_ratio(k)
            ratio_k1 = elliptic_ratio(k1) if k1 > 0 else 0
            q = ratio_k1 / ratio_k if ratio_k1 > 0 and ratio_k > 0 else 0.5
        eps_eff = 1 + (eps_r - 1)/2 * q
        Z0 = (30*np.pi / np.sqrt(eps_eff)) * elliptic_ratio(k)
        return {'Z0': Z0, 'eps_eff': eps_eff}

# Differential Microstrip
class DifferentialMicrostripAnalytical:
    @classmethod
    def analyze(cls, w, s, h, t=0, eps_r=4.2):
        wh, sh = w/h, s/h
        a, b = (eps_r+1)/2, (eps_r-1)/2
        F = (1+12/wh)**(-0.5) + (0.04*(1-wh)**2 if wh <= 1 else 0)
        eps_eff_s = a + b * F
        Z0_s = (120*np.pi/(2*np.pi*np.sqrt(eps_eff_s)))*np.log(8/wh+wh/4) if wh <= 1 else                120*np.pi/(np.sqrt(eps_eff_s)*(wh+1.393+0.667*np.log(wh+1.444)))
        if wh <= 1 and sh <= 1:
            cf = 0.2 * wh**2 / (sh + wh)
            Z0e = Z0_s / (1 + cf)
            Z0o = Z0_s * (1 - cf * 0.8)
        else:
            k_c = 0.5 * (np.tanh(1.2*sh**0.8))**2 * np.exp(-0.5*sh)
            Z0e = Z0_s / np.sqrt(1 + k_c)
            Z0o = Z0_s * np.sqrt(1 - k_c)
        return {'Z_diff': 2*Z0o, 'Z0_even': Z0e, 'Z0_odd': Z0o}

# Differential Stripline
class DifferentialStriplineAnalytical:
    @classmethod
    def analyze(cls, w, s, b, t=0, eps_r=4.2):
        arg_w = np.clip(np.pi*w/(2*b), -700, 700)
        arg_ws = np.clip(np.pi*(w+s)/(2*b), -700, 700)
        tanh_w = np.tanh(arg_w)
        tanh_ws = max(np.tanh(arg_ws), 1e-10)
        ke = np.clip(tanh_w * tanh_ws, 0, 1)
        ko = np.clip(tanh_w / tanh_ws, 0, 1)
        Z0e = (60/np.sqrt(eps_r)) * elliptic_ratio(ke)
        Z0o = (60/np.sqrt(eps_r)) * elliptic_ratio(ko)
        return {'Z_diff': 2*Z0o, 'Z0_even': Z0e, 'Z0_odd': Z0o}
