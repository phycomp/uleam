---
name: git-push
description: "Git 推送技能：從 commit 到 push 至 GitHub，含 PAT 設定、remote 設定、大檔案處理、workflow scope。Use when the user wants to push to GitHub, set up git remote, handle PAT, or troubleshoot push failures."
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---
# Git Push — 推送流程

## 流程

### 1. 帳號與憑證
- GitHub 帳號註冊 + email 驗證。
- 建立 PAT：GitHub → Settings → Developer settings → Personal access tokens → Generate new token (classic)。
- 勾選 scopes：`repo` + `workflow`（推送 .github/workflows 需 workflow scope）。
- 儲存 token 至 `~/.credentials`。

### 2. Git 設定
```bash
git config --global user.name "<username>"
git config --global user.email "<email>"
```

### 3. 建立 Repository
- 前往 https://github.com/new 建立 repo。
- 或用 API：`curl -X POST -H "Authorization: Bearer <PAT>" https://api.github.com/user/repos -d '{"name":"<repo>","private":false}'`

### 4. 設定 Remote
```bash
git init
git remote add origin https://github.com/<owner>/<repo>.git
```

### 5. 提交與推送
```bash
git add -A
git commit -m "feat: <description>"
TOKEN=$(cat ~/.credentials)
git push "https://<username>:${TOKEN}@github.com/<owner>/<repo>.git" main
```

### 6. 常見問題
- **Repository not found (404)**：repo 不存在，先建立。
- **Permission denied (403)**：PAT 缺少 `repo` 或 `Contents: Write` 權限。
- **workflow scope missing**：推送 .github/workflows 需 `workflow` scope。
- **Large file warning**：>50MB 檔案，考慮 Git LFS。
- **fetch first**：遠端有新提交，先 `git pull --rebase`。

### 觸發條件
- 「git push」「推送」「GitHub 推送」「commit and push」