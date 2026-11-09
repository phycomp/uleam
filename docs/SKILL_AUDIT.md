# 量子傳輸線技能盤點與整合狀態 (Skill Audit)

## 全域 (~/.opencode/skills/)
component-integration, generic-qcable, mantaro, nbtii-medium-batch, nbtii-pcb-fab, nbtii-r2r-mass, nbtii-small-batch, nbtii-test-sop, polar, quantum-cryogenic-cable, refactor, skill-generator, thermal-load-measurement, thermal-load-simulation, thermal-load-sop, thermal-load-units

## 專案 (/home/sam/代理人/.agents/skills/)
component-integration, generic-qcable, mantaro, nbtii-medium-batch, nbtii-pcb-fab, nbtii-r2r-mass, nbtii-small-batch, nbtii-test-sop, polar, quantum-cryogenic-cable, refactor, skill-generator, thermal-load-measurement, thermal-load-simulation, thermal-load-sop, thermal-load-units

## 量傳線 (/home/sam/量傳線/.opencode/skills/)
quantum-cryogenic-cable, refactor, skill-generator

## 量子傳輸線相關技能一覽
| 技能 | 說明 | 全域 | 代理人 | 量傳線 |
|------|------|------|--------|--------|
| generic-qcable | 通用型量子傳輸線設計/優化/重構 | ✅ | ✅ | — |
| quantum-cryogenic-cable | 依規格 CF3/FPC/Uleam1 計算 | ✅ | ✅ | ✅ |
| mantaro | Mantaro 風格阻抗計算器 | ✅ | ✅ | — |
| polar | Polar 模板採樣計畫 | ✅ | ✅ | — |
| component-integration | 衰減器/LPF/IR filter 整合 | ✅ | ✅ | — |
| thermal-load-* | 熱負載量測/模擬/單位/SOP | ✅ | ✅ | — |
| nbtii-* | NbTi 生產/測試 SOP | ✅ | ✅ | — |
| skill-generator | SKILL 產生器 | ✅ | ✅ | ✅ (原 qcable-spec 已統一) |
| refactor | 重構整合流程 | ✅ | ✅ | ✅ |

## 整合狀態
- 全域與代理人專案：已同步（16 個技能一致）。
- 量傳線專案：已補齊 skill-generator（原 qcable-spec 已移除），保留 quantum-cryogenic-cable 與 refactor。
- 缺口已補齊：mantaro、polar 已同步至代理人專案；refactor、quantum-cryogenic-cable 已全域佈署。

## 結論
整合完整。所有量子傳輸線相關技能已全域佈署且專案間一致。