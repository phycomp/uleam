---
name: ytauto
description: "YouTube 自動上傳技能：OAuth 授權、頻道核對、視頻上傳（unlisted/public/private）、排程、頻道管理（新增頻道）。Use when the user wants to upload to YouTube, manage YouTube channels, set up OAuth, or automate YouTube uploads."
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---
# ytauto — YouTube 自動上傳

## 功能
- OAuth 2.0 授權（`--auth` / `--auth-manual`）。
- 頻道核對（`--check`）：授權頻道必須等於目標頻道。
- 視頻上傳（`--slug` / `--all`），支援 `--privacy`（public/unlisted/private）、`--publish-at`、`--dry-run`。
- Playlist 建立與管理（需 `youtube` scope）。
- 音頻口白（TTS）：edge-tts（`make_shorts.py --voice`），支援中文多語音。
- 頻道管理：新增/切換頻道（見下方）。

## 音頻口白 (TTS)
使用 edge-tts 生成旁白：
```bash
cd /home/sam/ytauto
/home/sam/flex/bin/python scripts/make_shorts.py --slug <slug> --voice zh-TW-HsiaoChenNeural --rate +12%
```
支援語音：zh-TW-HsiaoChenNeural, zh-TW-YunJheNeural 等。

## 上傳至相關頻道
1. 建立/選擇目標頻道（Google Cloud Console + OAuth）。
2. 設定 `config.yaml` 中的 `channel_id`。
3. 執行 `--check` 確認頻道核對。
4. 執行 `--slug <slug> --privacy public`。

## 上傳至相關 Playlist
需 `youtube` scope（重新授權）。
```python
yt.playlists().insert(part='snippet,status', body={
    'snippet': {'title': 'Playlist Name', 'description': '...'},
    'status': {'privacyStatus': 'public'}
}).execute()
yt.playlistItems().insert(part='snippet', body={
    'snippet': {'playlistId': '<id>', 'resourceId': {'kind': 'youtube#video', 'videoId': '<vid>'}}
}).execute()
```

## 頻道與 Playlist
現有頻道：呂俊興 (UCGQja3bvv7PBxuZjqnC7Wkg)

播放清單：
- Oloid 3D 列印產品 (PLSUukGj3lAWs)
- AI (PLS6v73CYt3uU)
- 致富 (PLNMWTaoX0CLg)
- 量子演算法 (PLP4Q469W45KY)
- PQC 後量子密碼 (PLLlzzOFFobuc)
- QKD 量子金鑰分發 (PLFn6ms5gzn_k)

### 新增頻道
1. 在 Google Cloud Console 建立新專案（或使用現有）。
2. 啟用 YouTube Data API v3。
3. 建立 OAuth 用戶端 ID（桌面應用程式）。
4. 在 `config.yaml` 中新增頻道設定。
5. 執行 `--auth-manual --config <config>` 並指定頻道。
6. 執行 `--check` 確認頻道核對。

### 新增 Playlist
```python
yt.playlists().insert(part='snippet,status', body={
    'snippet': {'title': 'Playlist Name', 'description': '...'},
    'status': {'privacyStatus': 'public'}
}).execute()
```

## Playlist 建立
需 OAuth scope 包含 `https://www.googleapis.com/auth/youtube`（playlist 管理）。
```python
# 建立 playlist
yt.playlists().insert(part='snippet,status', body={
    'snippet': {'title': 'Playlist Name', 'description': '...'},
    'status': {'privacyStatus': 'public'}
}).execute()
# 加入視頻
yt.playlistItems().insert(part='snippet', body={
    'snippet': {'playlistId': '<playlist_id>',
                'resourceId': {'kind': 'youtube#video', 'videoId': '<video_id>'}}
}).execute()
```

## 公開狀態 (public)
- 上傳時設定 `--privacy public`。
- 或上傳後在 YouTube Studio 手動切換為公開。
- 排程公開：`--publish-at ISO8601`（需符合 YouTube 規則）。

## 常見問題
- **403 access_denied**：OAuth 同意畫面未加入測試使用者，或 User Type 為 Internal。
- **API 未啟用**：啟用 YouTube Data API v3。
- **頻道不符**：授權頻道 ≠ 目標頻道，中止上傳。
- **Playlist scope 不足**：需 `youtube` scope（非僅 `youtube.upload`）。
- **403 insufficientPermissions**：token 缺少 `youtube` scope，重新授權。

## 重新上傳視頻
1. 準備新的視頻檔案與 metadata。
2. 執行上傳：`--slug <slug> --privacy <status>`。
3. 確認上傳成功後，刪除舊的重複視頻（見下方）。

## 刪除重複視頻
需 `youtube` scope（或 Studio 手動刪除）。
```python
yt.videos().delete(id="<video_id>").execute()
```
或使用 YouTube Studio：https://studio.youtube.com → 選擇視頻 → 刪除。

## 重新上傳 + 刪除重複流程
1. 上傳新視頻（`--privacy unlisted`）。
2. 確認新視頻可播放。
3. 刪除舊的重複視頻。
4. 將新視頻設為 public（若需要）。
5. 更新 Playlist（移除舊視頻、加入新視頻）。

## 使用範例
```bash
cd /home/sam/ytauto
# 授權
/home/sam/flex/bin/python scripts/upload_youtube.py --auth-manual
# 核對頻道
/home/sam/flex/bin/python scripts/upload_youtube.py --check
# 上傳
/home/sam/flex/bin/python scripts/upload_youtube.py --slug oloid --privacy unlisted
# dry-run
/home/sam/flex/bin/python scripts/upload_youtube.py --slug oloid --dry-run
```

## 常見問題
- **403 access_denied**：OAuth 同意畫面未加入測試使用者，或 User Type 為 Internal。
- **API 未啟用**：啟用 YouTube Data API v3。
- **頻道不符**：授权頻道 ≠ 目標頻道，中止上傳。

## 觸發條件
- 「YouTube 上傳」「ytauto」「OAuth」「頻道管理」「新增頻道」