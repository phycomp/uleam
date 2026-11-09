# grok-build 使用與測試說明

## 1. 環境

- 二進位：`~/.grok/bin/grok` (v1.0.70)，已在 PATH
- 設定檔：`~/.grok/config.toml`
- 預設模型：`opencode-beam-free`

確認：
```bash
grok --version
grok models
```

## 2. 基本使用

### TUI 互動模式
```bash
cd /your/project
grok
```
啟動後預設使用 `opencode-beam-free`。切換模型：
```
/model opencode-big-pickle
/model opencode-beam-free
```
或按 `Ctrl+M` 開啟模型選擇器。

### Headless / 腳本模式
```bash
grok -p "你的提示" -m opencode-beam-free
grok -p "你的提示" -m opencode-big-pickle
```

### 指定工作目錄
```bash
grok -p "列出專案結構" --cwd /path/to/project
```

## 3. 模型說明

| Catalog key | 上游模型 | Endpoint | 費用 | 備註 |
|---|---|---|---|---|
| `opencode-big-pickle` | big-pickle | opencode personal | 免費 | 有每日免費額度，可能 `FreeUsageLimitError` |
| `opencode-beam-free` | beam-free | opencode go | 免費 | 需 `x-opencode-session` header (已設定) |

## 4. 測試流程

### 4.1 設定驗證
```bash
grok models
# 預期：列出 grok-4.7, opencode-big-pickle, opencode-beam-free (default)
```

### 4.2 Beam Free 推論測試 (應成功)
```bash
grok -p "reply with exactly: OK" -m opencode-beam-free
# 預期輸出：OK
```

### 4.3 Big Pickle 連線測試 (可能 rate-limited)
grok 對 429 會重試並可能卡住，建議直接用 curl 驗證端點：
```bash
curl -s -m 30 https://opencode.ai/inference/openai/v1/chat/completions \
  -H "Authorization: Bearer oc_sk_2ec02e175c00_yTQjxkTcULLJljrM_THGejclwP4C8OMH" \
  -H "x-opencode-org-id: org_01M63D7WQPNQJ7MC7Z318WPJD3" \
  -H "Content-Type: application/json" \
  -d '{"model":"big-pickle","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
# 成功：回傳 choices
# 失敗：FreeUsageLimitError (每日額度用盡，等待重置)
```

### 4.4 Headless 腳本測試
```bash
./grok_opencode.sh
```

### 4.5 TUI 測試
1. 執行 `grok`
2. 輸入 `/model opencode-beam-free`
3. 提問：「請用一句話說明這個 repo」
4. 確認回應正常、無錯誤

### 4.6 除錯
```bash
RUST_LOG=debug GROK_LOG_FILE=/tmp/grok.log grok -p "hi" -m opencode-beam-free
tail -f /tmp/grok.log
```
查找 `model` / `sampling` / `429` / `FreeUsage`。

## 5. 常見問題

- **FreeUsageLimitError (big-pickle)**：每日免費額度用盡，切換到 beam-free 或等待重置。
- **MissingSessionID (beam-free)**：確認 config 中 `extra_headers` 含 `x-opencode-session`。
- **401 Unauthorized**：API key 過期/錯誤，更新 `api_key`。
- **模型不存在**：執行 `grok models` 確認 catalog key。

## 6. 設定備份/還原
```bash
# 備份
cp ~/.grok/config.toml ~/.grok/config.toml.bak
# 還原
cp ~/.grok/config.toml.bak ~/.grok/config.toml
```
