---
name: electrical-spec
description: Use when the user wants to define or review electrical specifications/acceptance criteria for a transmission line or component (impedance, frequency range, loss, return loss/VSWR, phase stability, crosstalk, thermal constraints), or asks to 電性規格、electrical spec、阻抗/VSWR/損耗規格、驗收條件.
---

# Electrical Specification Capability（可移植）

本 skill 定義**電性規格與驗收條件**的結構。規範用中性佔位（6B）；公開單位（Ω、GHz、dB、° 等）與通用 SOP 結構可保留。

## 規格表（範本）
| 項目 | 規格/門檻 | 條件/方法 | 備註 |
|---|---|---|---|
| 特徵阻抗 | `<z0_target>` ± `<tol>` | `<method>`、溫區/條件 | |
| 頻率範圍 | `<f_min>`–`<f_max>` | | |
| 插入損耗/衰減 | `<il_limit>` @ `<condition>` | | |
| 反射/VSWR/return loss | `<rl_vswrlimit>` | | |
| 相位穩定性 | `<phase_limit>`（條件） | 循環/溫變 | |
| 串擾 | `<crosstalk_limit>`（NEXT/FEXT） | 鄰道/條件 | |
| 熱/功率約束（如適用） | `<thermal_limit>` | 溫區 | |

## 驗收條件（最小集）
- 常溫/指定條件電性：關鍵指標達門檻，方法與證據可追溯。
- 環境/低溫（如適用）：在定義溫區/循環下驗證。
- 未達門檻或缺證據 → 不得宣稱符合規格。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Gate rule、Evidence 最小欄位、Stop-the-line、Change control。規格/KPI 變更需版本化並重驗。

## 交棒（capability）
- 計算/模擬 → `design simulation capability`；測試執行 → `test/SOP capability`；裁決 → `acceptance/KPI gate capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。原專案可能含具體數值門檻；採用時應確認是否為可公開標準或需依 6B/專案授權處理。 مثال threshold forms: impedance 50Ω-class, VSWR/return-loss limits, loss/crosstalk/phase limits by condition.