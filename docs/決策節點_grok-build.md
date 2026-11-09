# 決策節點：grok-build 安裝與 opencode LLM 外接

## 節點 1：安裝來源
- 問題：grok 二進位檔已存在 (~/.grok/bin/grok v1.0.70)，是否重裝/建置？
- 決策：**保留現有二進位** (PATH 已包含 ~/.grok/bin)
- 建議：避免重裝；rust/cargo 未安裝，從原始碼建置不可行。

## 節點 2：客製化範圍
- 問題：調整哪些設定？
- 決策：**完整客製化**
- 子決策：
  - 2a Permission mode：**ask** (每次工具呼叫前詢問)
  - 2b Sandbox：**啟用** (profile = workspace)
  - 2c UI/Theme：**保持預設** (compact_mode false, max_thoughts_width 120)
- 建議：安全優先；sandbox 隔離 shell，permission ask 避免誤操作。

## 節點 3：opencode LLM 外接
- 問題：啟用哪些 opencode 模型？
- 決策：**兩者都啟用，預設 beam-free**
- 模型：
  - opencode-big-pickle：personal endpoint https://opencode.ai/inference/openai/v1，免費但有每日限制 (FreeUsageLimitError)
  - opencode-beam-free：go endpoint https://opencode.ai/inference/go/openai/v1，免費無限，需 x-opencode-session header
- 建議：beam-free 為預設 (穩定/無限)；big-pickle 備用 (可能 rate-limited)。

## 節點 4：認證儲存
- 問題：opencode API key 如何存放？
- 決策：**寫入 config.toml** (api_key 明文)
- 建議：本機個人使用可接受；key = oc_sk_2ec02e175c00_...，org header = org_01M63D7WQPNQJ7MC7Z318WPJD3。

## 實作結果
- ~/.grok/config.toml 已更新
- 驗證：`grok models` 顯示 opencode-big-pickle / opencode-beam-free (default)
- 驗證：`grok -p "reply OK" -m opencode-beam-free` 回傳 OK
- big-pickle 目前 rate-limited (FreeUsageLimitError)，待限制解除後可用

## 注意事項
- opencode-go (beam-free) 需穩定 x-opencode-session header，已設為 "grok-opencode-session"
- big-pickle (personal) 不需 session header，但仍受每日免費額度限制
- API key 明文存放，請勿分享 config.toml
