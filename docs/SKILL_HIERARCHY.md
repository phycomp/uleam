# 量子傳輸線技能層級架構 (Skill Hierarchy)

## 主技能（Core / Primary）
| 技能 | 說明 | 依賴 |
|------|------|------|
| generic-qcable | 通用型量子傳輸線設計/計算/優化/重構 | 無（基礎） |
| quantum-cryogenic-cable | 依規格 CF3/FPC/Uleam1 計算 | generic-qcable（概念） |
| qcable-index | 技能索引與導航 | 所有技能 |

## 次技能（Supporting / Secondary）
### 計算與設計
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| mantaro | quantum-cryogenic-cable | 阻抗計算器 UI |
| polar | quantum-cryogenic-cable | 採樣計畫 |
| component-integration | generic-qcable | 衰減器/LPF/IR filter |
| connector | component-integration | 連接器選型與測試 |

### 熱負載
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| thermal-load-measurement | generic-qcable | 量測 |
| thermal-load-simulation | generic-qcable, 計算.py | 模擬 |
| thermal-load-units | thermal-load-simulation | 單位轉換 |
| thermal-load-sop | thermal-load-measurement | 量測 SOP |

### 生產與 SOP
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| nbtii-small-batch | quantum-cryogenic-cable | 小量生產 |
| nbtii-pcb-fab | nbtii-small-batch | 板廠 |
| nbtii-medium-batch | nbtii-pcb-fab | 中量生產 |
| nbtii-r2r-mass | nbtii-medium-batch | 大量生產 |
| nbtii-test-sop | nbtii-small-batch | 生產測試 |

### 工具與流程
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| skill-generator | 無（meta） | 產生技能 |
| refactor | 無（meta） | 重構流程 |
| cloud-deploy | 無（infra） | 雲端佈署 |

## 依賴關係圖
```
generic-qcable (基礎)
├── quantum-cryogenic-cable
│   ├── mantaro
│   ├── polar
│   ├── nbtii-small-batch
│   │   ├── nbtii-pcb-fab
│   │   │   └── nbtii-medium-batch
│   │   │       └── nbtii-r2r-mass
│   │   └── nbtii-test-sop
│   └── component-integration
│       └── connector
├── thermal-load-measurement
│   ├── thermal-load-simulation
│   │   └── thermal-load-units
│   └── thermal-load-sop
└── qcable-index (索引所有)
```

## 三視圖模組（三視圖.py）
- `繪製前視圖(spec, ...)`：前視圖（X-Y 截面）
- `繪製側視圖(spec, ...)`：側視圖（Z-Y 剖面）
- `繪製上視圖(spec, ...)`：上視圖（X-Z 俯視）
- `繪製全部視圖(spec)`：一次產生三視圖
- `設定字型(ax, size)`：獨立字型設定
- `設定縮放(ax, zoom)`：獨立縮放控制