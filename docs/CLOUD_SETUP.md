# 雲端佈署指南 (Cloud Setup)

## 1. 建立帳號

### GitHub
1. 前往 https://github.com/signup
2. 註冊帳號，驗證 email。
3. 建立 repository（代理人 / 量傳線）。

### Cloudflare
1. 前往 https://dash.cloudflare.com/sign-up
2. 註冊帳號，驗證 email。
3. 取得 Account ID：Dashboard → 右側 "Account ID"。
4. 建立 API Token：My Profile → API Tokens → Create Token → "Edit Cloudflare Workers" template，加入 Containers 權限。

## 2. 設定 GitHub Secrets
在每個 repository → Settings → Secrets and variables → Actions，新增：
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

## 3. 建立 GitHub Repository
1. 前往 https://github.com/new
2. Repository name：`quantum-transmission-line`（代理人）/ `liangchuan-line`（量傳線）
3. 選擇 Public/Private，點 Create repository。

## 4. 建立 Personal Access Token (PAT)
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token.
2. 勾選 `repo`、`workflow` 權限。
3. 複製 token（只顯示一次）。

## 5. 推送程式碼
```bash
cd /home/sam/代理人  # 或 /home/sam/量傳線
git add .
git commit -m "initial"
git push -u origin main
# Username: ontxac
# Password: <貼上 PAT>
```
或使用 credential helper 儲存：
```bash
git config --global credential.helper store
git push -u origin main
```

## 4. 自動佈署
Push 後 GitHub Actions 自動執行 `wrangler deploy`，佈署至 Cloudflare Containers。

> 本機部署需 Docker + buildx。若本機缺少 buildx，請使用 GitHub Actions（Ubuntu runner 已內建 Docker）。

## 4b. 本機部署（可選）
```bash
sudo pacman -S docker-buildx
docker build -t quantum-transmission-line:latest .
wrangler deploy
```

## 6. Render 佈署（替代 Cloudflare）
1. 前往 https://render.com → Sign up（可用 GitHub 帳號）。
2. New → Web Service → 連接 GitHub repo。
3. Render 自動偵測 `render.yaml`，點 Create Web Service。
4. 等待 build 完成，取得 URL。

## 7. Railway 佈署（替代 Cloudflare）
1. 前往 https://railway.app → Login with GitHub。
2. New Project → Deploy from GitHub repo。
3. Railway 自動偵測 `railway.toml` / Dockerfile。
4. 設定環境變數，點 Deploy。

## 5. 手動佈署（本機）
```bash
npm install -g wrangler
wrangler login          # 會開啟瀏覽器 OAuth
wrangler deploy
```

### 瀏覽器 OAuth（Moli）
本環境已安裝 Moli 瀏覽器（`~/.local/bin/moli`，v1.1.21），可用於 headless OAuth：
```bash
moli fetch https://dash.cloudflare.com/oauth2/auth?...
```
或啟動 CDP server：
```bash
moli serve --port 9222
```

## 6. 驗證
- Cloudflare Dashboard → Workers & Pages → 確認服務運行。
- 存取 `https://<worker-name>.<subdomain>.workers.dev`。

## 注意事項
- Streamlit 需容器執行（Cloudflare Containers），非 Pages 靜態。
- 首次佈署需等待映像建置（數分鐘）。
- 量傳線需 Dockerfile.slim（無 LibreOffice）以縮小映像。