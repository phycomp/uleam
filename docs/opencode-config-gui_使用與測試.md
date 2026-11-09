# opencode-config-gui 使用與測試說明

## 1. 環境

- 專案路徑：`/home/sam/代理人/opencode-config-gui`
- Binary：`target/debug/opencode-config-gui` / `target/release/opencode-config-gui`
- Rust toolchain：rustup stable (1.99.1)

確認：
```bash
cd /home/sam/代理人/opencode-config-gui
source $HOME/.cargo/env
cargo --version
```

## 2. 基本使用

### GUI 模式 (需顯示環境)
```bash
./target/release/opencode-config-gui
```
分頁：OpenCode / Grok / CrewAI。支援搜尋框過濾。按 "Fetch live schema" 從上游更新；按 "Export Markdown" 匯出報告到 `~/opencode_config_report.md`。

### Headless 匯出
```bash
./target/release/opencode-config-gui --dump               # stdout
./target/release/opencode-config-gui --export out.md     # 寫檔
./target/release/opencode-config-gui --help
```

## 3. 資料來源

| 檔案 | 內容 |
|---|---|
| data/opencode_schema.json | OpenCode config.json schema (49 top-level + AgentConfig) |
| data/opencode_agents.json | 內建 agents (Build/General/Explore/Compaction/Title/Summary/Plan) |
| data/grok_config.json | Grok config.toml 56 sections / 410 keys |
| data/grok_agents.json | Grok bundled agents (explore/general-purpose/plan) |
| data/crewai_agent.json | CrewAI Agent 63 fields |

## 4. 測試流程

### 4.1 Build 驗證
```bash
cargo build 2>&1 | tail -3
cargo build --release 2>&1 | tail -3
# 預期：Finished
```

### 4.2 Headless dump
```bash
./target/debug/opencode-config-gui --dump | head -20
# 預期：# OpenCode / Grok / CrewAI Config & Agent Settings
```

### 4.3 匯出檔案
```bash
./target/debug/opencode-config-gui --export /tmp/opencode/report.md
wc -l /tmp/opencode/report.md
# 預期：~699 行
```

### 4.4 內容抽查
```bash
grep -c "OpenCode — top-level settings" /tmp/opencode/report.md
grep -c "Grok — config sections" /tmp/opencode/report.md
grep -c "CrewAI — Agent fields" /tmp/opencode/report.md
# 預期：各 1
```

### 4.5 Live schema fetch (需網路)
GUI 按 "Fetch live schema"，狀態列顯示 "Fetched live schema OK"。

### 4.6 GUI 顯示 (需顯示環境)
在有 X11/Wayland 的環境執行 binary，確認三 tab 可切換、搜尋可過濾、折疊展開正常。

## 5. 常見問題

- **GUI 無法啟動 (MESA/ZINK)**：headless 環境無 GPU；用 --dump/--export 替代，或在有顯示的機器執行。
- **schema 過舊**：按 Fetch live schema 更新，或重新下載 data/opencode_schema.json。
- **編譯失敗 (缺系統函式庫)**：安裝 build-essential、libgtk-3-dev、libxcb-render0-dev、libxcb-shape0-dev、libxcb-xfixes0-dev、libxkbcommon-dev、libssl-dev。

## 6. 重新建置
```bash
source $HOME/.cargo/env
cargo clean && cargo build --release
```