# OpenCode Route + Workers 設計

## 架構

```
┌─────────────────────────────────────────┐
│  Router Agent (main)                     │
│  - 接收使用者請求                        │
│  - 分析任務類型 → 路由至對應 Worker      │
│  - 彙整 Worker 結果 → 回覆使用者         │
└────────────┬────────────────────────────┘
             │
    ┌────────┼────────┬────────┬────────┐
    ▼        ▼        ▼        ▼        ▼
┌───────┐┌───────┐┌───────┐┌───────┐┌───────┐
│Planner││Coder  ││Tester ││Review ││Worker │
│(plan) ││(edit) ││(test) ││(rev)  ││(task) │
└───────┘└───────┘└───────┘└───────┘└───────┘
```

## Worker Pool

| Worker | Mode | 職責 | 權限 |
|--------|------|------|------|
| planner | subagent | 探索程式碼、產生實作計畫 | read/glob/grep/web |
| coder | subagent | 編輯程式碼、實作功能 | read/edit/shell |
| tester | subagent | 執行測試、報告失敗 | read/shell/edit(tests) |
| reviewer | subagent | 審查正確性/安全性/測試 | read/glob/grep |
| worker | subagent | 通用任務執行 | read/edit/shell/glob/grep |

## 路由規則

| 請求類型 | 路由至 |
|----------|--------|
| "設計/規劃" | planner |
| "實作/修改" | coder |
| "測試" | tester |
| "審查/檢查" | reviewer |
| "通用任務" | worker |

## 設定檔

`~/.config/opencode/opencode.jsonc` → `agents` 區塊新增 router + worker。

## 觸發
- 「route+workers」「路由工作者」「OpenCode 架構」