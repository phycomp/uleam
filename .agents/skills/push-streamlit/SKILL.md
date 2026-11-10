---
name: push-streamlit
description: "Streamlit 網站推送技能：從本地開發 → GitHub 推送 → Streamlit Cloud 部署，含 credentials 設定與常見問題。Use when the user wants to push a Streamlit website to GitHub and deploy to Streamlit Cloud."
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---
# Push Streamlit — 網站推送與部署

## 流程

### 1. 本地開發
- 建立 Streamlit 應用（`app.py` + `pages/` + `requirements.txt`）。
- 使用相對路徑引用資產（避免雲端路徑錯誤）。
- 本地測試：`streamlit run app.py`。

### 2. Git 設定
```bash
git config --global user.name "<username>"
git config --global user.email "<email>"
git init
git remote add origin https://github.com/<owner>/<repo>.git
```

### 3. Credentials
- GitHub PAT 儲存於 `~/.credentials`（一行，僅 token 值）。
- 推送時：`TOKEN=$(cat ~/.credentials)`。

### 4. 提交與推送
```bash
git add -A
git commit -m "feat: <description>"
TOKEN=$(cat ~/.credentials)
git push "https://<username>:${TOKEN}@github.com/<owner>/<repo>.git" main
```

### 5. Streamlit Cloud 部署
1. 前往 https://share.streamlit.io → Sign in with GitHub。
2. New app → 選擇 repo → Branch: main → Main file: `app.py`。
3. Deploy! → 取得 URL（如 `https://<app>.streamlit.app`）。

### 6. 驗證
- `python examples/test_deployed.py <base_url>`
- 檢查 `/_stcore/health`（HTTP 200）。
- 若 303 redirect → 設定 Sharing 為 Public。

### 常見問題
- **ModuleNotFoundError**：requirements.txt 缺少依賴。
- **FileNotFoundError**：使用絕對路徑 → 改為相對路徑。
- **303 redirect**：應用設為私有 → Settings → Sharing → Public。
- **Large file**：>100MB 檔案需 Git LFS。

### 觸發條件
- 「push streamlit」「推送網站」「streamlit deploy」「GitHub 推送」