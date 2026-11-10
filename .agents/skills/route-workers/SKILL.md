---
name: route-workers
description: "OpenCode Route+Workers 設計技能：路由分派任務給 worker subagents（planner/coder/tester/reviewer/worker），含設定與使用指南。Use when the user wants to set up OpenCode as route+workers, configure subagents, or design a router-worker architecture."
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---
# Route + Workers — OpenCode 路由工作者架構

## 架構
```
Router (primary) → dispatch → Worker Pool (subagents)
```

## Worker Pool
| Worker | 職責 | 權限 |
|--------|------|------|
| planner | 探索程式碼、產生計畫 | read/glob/grep/web |
| coder | 編輯程式碼、實作功能 | read/edit/shell |
| tester | 執行測試、報告失敗 | read/shell/edit(tests) |
| reviewer | 審查正確性/安全性 | read/glob/grep |
| worker | 通用任務執行 | read/edit/shell/glob/grep |

## 路由規則
| 請求類型 | 路由至 |
|----------|--------|
| "設計/規劃" | planner |
| "實作/修改" | coder |
| "測試" | tester |
| "審查/檢查" | reviewer |
| "通用任務" | worker |

## 設定檔
`~/.config/opencode/opencode.jsonc` → `agents` 區塊。

## 觸發條件
- 「route+workers」「路由工作者」「OpenCode 架構」「subagent」
