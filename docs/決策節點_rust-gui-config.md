# 決策節點：Rust GUI — OpenCode/Grok/CrewAI 設定與 Agent 組態瀏覽

## 節點 1：GUI 框架
- 問題：用哪個 Rust GUI 框架？
- 決策：**egui/eframe** (Immediate-mode，單一 binary)
- 建議：學習曲線低，適合設定瀏覽器；單一 binary 易散佈。

## 節點 2：資料來源
- 問題：opencode 設定清單從哪裡取得？
- 決策：**執行時抓取 schema** (https://opencode.ai/config.json) + 本機快取，離線回退到內嵌 bundled schema
- 建議：保持與上游同步；無網路時仍可用。

## 節點 3：Agent 設定範圍
- 問題：「找出所有 agent 設定組態」指什麼？
- 決策：**opencode + grok + crewAI 三者**
- 資料：
  - opencode：schema AgentConfig 欄位 + /api/agent 內建 agents
  - grok：config.toml [agent] + bundled agents (explore/general-purpose/plan)
  - crewAI：Agent model_fields (63 欄位)
- 建議：跨框架統一瀏覽，便於比較。

## 節點 4：輸出/功能
- 問題：除了顯示還需要？
- 決策：**顯示 + 匯出 Markdown/JSON**
- 建議：瀏覽樹狀/分頁 + --export/--dump CLI 供 headless 測試。

## 節點 5：Rust 工具鏈
- 問題：cargo/rustc 未安裝
- 決策：**安裝 rustup** (stable toolchain)
- 建議：rustup 自動管理 toolchain，後續 cargo build 即可。

## 實作結果
- 專案路徑：`/home/sam/代理人/opencode-config-gui`
- Binary：`target/debug/opencode-config-gui`、`target/release/opencode-config-gui`
- 資料：data/*.json (opencode_schema, opencode_agents, grok_config, grok_agents, crewai_agent)
- CLI：--dump (stdout)、--export <path>、--help
- 驗證：--export 產生 699 行 Markdown 報告；--dump 正常輸出
- GUI 無法在此 headless 環境顯示 (MESA/ZINK 無 GPU)，需在有顯示的環境執行
