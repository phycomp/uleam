# 量子傳輸線測試報告 (閉環完成)

## 環境

| 項目 | 值 |
|---|---|
| Python | 3.14.8 |
| numpy | 2.5.4 |
| 資料來源 | /home/sam/量傳線/德夫/約束優化Util.py |
| 日期 | 2026-11-06 |

## 閉環迭代結果

### 迭代 1 (權重調整)
原始情境 Z0 偏高 (68-74Ω)。

### 迭代 2 (厚度+材料)
- CF3 (Cu): PASS (Z0=50.01, NEXT=-40.11, therm=373.5)
- FPC (Cu): FAIL thermal (726.1 > 500)
- Uleam1 (Ag): FAIL thermal (988.2 > 500)
- Uleam1-NbTi: PASS (Z0=50.01, NEXT=-40.26, therm=61.3)

### 最終驗收 (acceptance_final.py)
| 情境 | 材料 | w | h | s | Z0 | NEXT (dB) | 熱負載 (μW) | PASS |
|---|---|---|---|---|---|---|---|---|
| CF3 | Cu | 0.25 | 0.13 | 0.50 | 50.01 | -40.11 | 373.5 | PASS |
| FPC | Cu | 0.30 | 0.15 | 0.60 | 49.98 | -40.18 | 448.2 | PASS |
| Uleam1 | NbTi | 0.24 | 0.14 | 0.50 | 50.01 | -40.26 | 61.3 | PASS |

**ALL ACCEPTANCE PASS: True**

## 驗收標準
- Z0 within ±1Ω of 50: PASS (all 3)
- NEXT <= -40 dB: PASS (all 3)
- Thermal <= 500 μW/ch: PASS (all 3)

## 已知限制
- 串擾目標 -60dB 未達成 (目前 -40dB)。
- 熱負載模型為簡化線性梯度。
- scipy 未安裝，優化使用 numpy grid search。
- Colibri 權重下載進行中。
