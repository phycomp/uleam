# 決策節點：opencode 主要設定檔與客製化

## 節點 1：設定檔範圍
- 問題：客製化哪些 opencode 設定檔？
- 決策：**全域 + 專案層**
- 實作：
  - 全域：`~/.config/opencode/opencode.jsonc`
  - 專案層：`/home/sam/代理人/opencode.jsonc`
- 建議：全域為基礎，專案層覆寫/補充。

## 節點 2：客製化目標
- 問題：優先調整哪些項目？
- 決策：**完整客製化**
- 內容：model、permissions、compaction、experimental、formatter、watcher、instructions、agents。

## 節點 3：預設模型
- 問題：預設模型？
- 決策：**opencode-go/beam-free**
- 建議：免費無限、穩定；small_model 同步設定。

## 節點 4：權限模式
- 問題：tool 權限策略？
- 決策：**permissive** (allow read/edit/shell/subagent 等)
- 建議：個人開發效率優先；reviewer/planner/tester 以 deny-first 再 allow 例外。

## 節點 5：自訂 Agent
- 問題：定義哪些自訂 agent？
- 決策：**reviewer / planner / tester** (subagent)
- 建議：reviewer 唯讀；planner 唯讀規劃；tester 可跑測試與編輯 test/**。

## opencode 主要設定檔清單
1. `~/.config/opencode/opencode.json(c)` — 全域使用者設定 (主要)
2. `~/.config/opencode/cli.json` — CLI/TUI 偏好 (theme、keybinds) [目前未建立]
3. `<project>/opencode.json(c)` — 專案根目錄設定
4. `<project>/.opencode/opencode.json(c)` — 專案 .opencode 目錄設定
5. `/etc/opencode/opencode.json` — 系統層 (machine-wide) [目前不存在]
6. `~/.config/opencode/agents/*.md`, `commands/*.md`, `skills/*/SKILL.md`, plugins — 檔案式定義
7. `<project>/.opencode/agents/*.md` 等 — 專案層檔案式定義
8. `AGENTS.md` (專案根) — 專案指令 (instructions)

## 實作結果
- 全域 config：已寫入，schema 驗證通過
- 專案 config：已寫入，schema 驗證通過
- opencode 載入驗證：model=opencode-go/beam-free，agents=reviewer,planner,tester，permissions=9
- 備份：`~/.config/opencode/opencode.jsonc.bak.*`
