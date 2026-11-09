# Agent Inference Policy

## Allowed (允許模糊推論範疇)
- 決定預設的逾時時間 (Timeout)
- 日誌訊息 (Log message) 的格式與字串串接
- 內部變數的臨時命名

## Blocked (絕對禁止推論，必須報錯中斷)
- 自行發明或修改資料庫 Schema、資料表或欄位名稱
- 自行推論外部 API 金鑰 (Secret Keys) 或驗證機制 (Auth Protocols)
- 修改既有的安全權限控管邏輯
