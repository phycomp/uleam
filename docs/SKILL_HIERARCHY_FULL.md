# 技能層級架構 (Skill Hierarchy)

## 一、量子傳輸線技能 (Quantum Transmission Line)

### 主技能 (Primary)
| 技能 | 說明 |
|------|------|
| generic-qcable | 通用型量子傳輸線設計/計算/優化/重構 |
| quantum-cryogenic-cable | 依規格 CF3/FPC/Uleam1 計算 |
| qcable-index | 技能索引與導航 |

### 次技能 (Secondary) — 計算與設計
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| mantaro | quantum-cryogenic-cable | 阻抗計算器 UI |
| polar | quantum-cryogenic-cable | 採樣計畫 |
| component-integration | generic-qcable | 衰減器/LPF/IR filter |
| connector | component-integration | 連接器選型與測試 |
| crosstalk-calc | generic-qcable | 串擾計算 |
| three-view | generic-qcable | 三視圖（前/側/上） |
| material-db | generic-qcable | 材質數據庫與驗收 |

### 次技能 — 熱負載
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| thermal-load-measurement | generic-qcable | 量測 |
| thermal-load-simulation | generic-qcable | 模擬 |
| thermal-load-units | thermal-load-simulation | 單位轉換 |
| thermal-load-sop | thermal-load-measurement | 量測 SOP |

### 次技能 — 電性規格與測試
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| electrical-spec | generic-qcable | 電性規格 |
| electrical-test-sop | electrical-spec | 電性測試 SOP |

### 次技能 — SOP 與生產
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| nbtii-small-batch | quantum-cryogenic-cable | 小量生產 |
| nbtii-pcb-fab | nbtii-small-batch | 板廠 |
| nbtii-medium-batch | nbtii-pcb-fab | 中量生產 |
| nbtii-r2r-mass | nbtii-medium-batch | 大量生產 |
| nbtii-test-sop | nbtii-small-batch | 生產測試 |

### 次技能 — 工具與流程
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| llm-parser | generic-qcable | LLM 自然語法解析 |
| measurement-unit-link | generic-qcable | 量測單位鏈結 |
| skill-generator | 無（meta） | 產生技能 |
| refactor | 無（meta） | 重構流程 |
| cloud-deploy | 無（infra） | 雲端佈署 |
| engineering-delivery | 無（meta） | 通用工程交付 pipeline |
| kpi-delivery-valid | engineering-delivery | KPI 交付驗證 |
| txt-proc / txt-genoffice | 無（tool） | 文件轉換 |
| material-db | generic-qcable | 材質數據庫 |
| three-view | generic-qcable | 三視圖 |
| oloid-3d-product | 無（product） | Oloid 3D 產品 |

### 依賴關係圖
```
generic-qcable (基礎)
├── quantum-cryogenic-cable
│   ├── mantaro
│   ├── polar
│   ├── nbtii-small-batch → nbtii-pcb-fab → nbtii-medium-batch → nbtii-r2r-mass
│   │   └── nbtii-test-sop
│   └── component-integration → connector
├── thermal-load-* (measurement/simulation/units/sop)
├── electrical-spec → electrical-test-sop
├── crosstalk-calc
├── three-view
├── material-db
├── llm-parser
├── measurement-unit-link
└── qcable-index (索引所有)
```

## 二、YouTube 技能
| 技能 | 位置 | 說明 |
|------|------|------|
| youtube-automation | ~/.agents/skills/ | YouTube 內容自動化 |
| youtube-oauth-upload | ~/.agents/skills/ | OAuth 上傳 |
| youtube-studio-browser-upload | ~/.agents/skills/ | Studio 瀏覽器上傳 |
| youtube-studio-browser-upload (ytauto) | /home/sam/ytauto | 上傳診斷 |

## 三、Git 技能
| 技能 | 位置 | 說明 |
|------|------|------|
| git-commit-and-push | ~/.agents/skills/ | 自動 commit & push |
| auto-commit | (search result) | 自動 commit/push/PR |
| pm-autofix-pr | (search result) | 自動修復 PR |
| refactor | ~/.opencode/skills/ | 重構整合流程 |

## 四、總覽
- 全域技能目錄：~/.opencode/skills/ (32) + ~/.agents/skills/ (377)
- 專案技能目錄：/home/sam/代理人/.agents/skills/ (120)
- 量子傳輸線相關：24 個技能（見 qcable-index）