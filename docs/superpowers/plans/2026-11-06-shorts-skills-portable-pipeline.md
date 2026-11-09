# Shorts Skills 可移植化與全流程沉澱 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 `~/ytauto` 的投資/財經 Shorts 全流程（製作→驗收→文案/上傳包→YouTube 上傳/核對→每週維運）與已知卡點處理，沉澱為 6 個可移植的全域 skills，並對既有腳本做最小必要的介面/契約規範化與止血修正。

**Architecture:** 以「全域 skill = 可移植操作手冊 + 明確契約」為主，`~/ytauto` 腳本為參考實作。新增一份可被所有腳本共用的設定載入層（CLI > env > 專案設定檔 > 預設），統一路徑/頻道/OAuth/瀏覽器 profile/排程欄位；上傳腳本在載入設定後維持既有 `--all/--slug` 等核心用法相容。YouTube 瀏覽器上傳加入 `video-id`/「儲存中」逾時止血與存證；OAuth/瀏覽器路線共用 `upload_result.json`/`upload_summary.json` schema。skills 拆分為 pipeline、production、acceptance、browser-upload、oauth-upload、troubleshooting 六個獨立單元。

**Tech Stack:** Python 3.14 venv (`/home/sam/代理人/.venv`)、ffmpeg/ffprobe、Pillow、edge-tts、Playwright Chromium、google-api-python-client/google-auth-oauthlib、Markdown skill files (`~/.agents/skills/<id>/SKILL.md`)、JSON 設定/結果檔。

**Spec:** 本對話確認之決策（2026-11-06）。關鍵事實：頻道 `UCGQja3bvv7PBxuZjqnC7Wkg`「呂俊興」；2 支已上傳 unlisted（`dS7b3meDYQg`、`N2vPVgdDggI`）；gcloud ADC/scope 路線不可用；`upload_youtube.py` 需自有 `client_secret.json` 且 OAuth app `qcryo` 目前有同意畫面驗證/測試使用者阻擋；Studio 瀏覽器路線曾成功，後續出現「儲存中…」無 `video-id`、`#next-button` hidden 的阻塞（含 3 秒測試片重現）。

## Global Constraints

- **語言：** skill 與計畫以**繁體中文（台灣）**為主，保留必要英文術語/指令/檔名/JSON key。
- **位置：** 6 個 skill 全部寫入全域 `~/.agents/skills/<id>/SKILL.md`：`shorts-pipeline`、`shorts-production`、`shorts-acceptance`、`youtube-studio-browser-upload`、`youtube-oauth-upload`、`shorts-upload-troubleshooting`。
- **可移植：** 不得硬編僅適用單機的路徑/頻道/憑證；以設定契約參數化，並提供 `~/ytauto` 相容預設。
- **相容性：** 現有 `cd ~/ytauto && python scripts/make_shorts.py|verify_shorts.py|upload_browser.py|upload_youtube.py --all|--slug ...` 核心用法必須維持可用（預設值/自動偵測）。
- **設定優先序：** `CLI 參數 > 環境變數 > 專案設定檔 > 內建預設`（E1）。
- **安全/真實性：** 驗收未 PASS 必須拒絕上傳；頻道不符必須中止；瀏覽器上傳在無 `video-id`/「儲存中」逾時或無法確認狀態時必須止血、存證、**不得宣稱成功**；不得盲目重試製造草稿。
- **隱私預設：** 上傳預設 `unlisted`；不自動轉 `public`（金融內容需人工確認）。
- **憑證：** 不提交/不列印 `client_secret.json`、`token.json`、瀏覽器 profile 敏感內容；文件只描述路徑與權限。
- **已知限制處理（D1+D2）：** 誠實記錄 `qcryo` 同意畫面/Test users 阻擋、Studio「儲存中…」無 `video-id`；本次實作 F2–F5 止血/契約/可移植化，並在文件與 plan 中保留未解項與建議修正。
- **排程（S2）：** 定義排程/`publishAt`/每週支數/平台清單欄位與語意；提供 cron/systemd timer 範本；不自動部署排程器。`publishAt` 瀏覽器路線標註可靠性風險；API 路線遵循 YouTube 狀態限制。

## Config Contract（目標契約，F2 實作）

設定檔建議路徑：`<workspace>/.ytauto/config.json`（優先）或 `<workspace>/ytauto.config.json`。環境變數前綴 `YTAUTO_`。

| 欄位 | 說明 | 預設/相容 |
|---|---|---|
| `workspace_root` | 專案根目錄 | 自動偵測（含 `content/`、`scripts/`）或 cwd |
| `content_dir` | 內容規格目錄 | `<workspace>/content` |
| `output_dir` | 成品目錄 | `<workspace>/output` |
| `python_bin` / `venv_python` | Python 路徑 | 目前直譯器 |
| `channel_id` | YouTube 頻道 ID | `UCGQja3bvv7PBxuZjqnC7Wkg`（相容） |
| `channel_name` | 頻道名稱 | `呂俊興` |
| `privacy_default` | 預設隱私 | `unlisted` |
| `browser_profile_dir` | Playwright profile | `~/.config/ytauto/browser-profile` |
| `client_secret_path` | OAuth client secret | `~/.config/ytauto/client_secret.json` |
| `token_path` | OAuth token | `~/.config/ytauto/token.json` |
| `locale` | 語言地區 | `zh-TW` |
| `timezone` | 排程時區 | `Asia/Taipei` |
| `weekly_target` | 每週支數 | `2` |
| `platforms` | 平台清單 | `["youtube_shorts","tiktok","instagram","linkedin","x"]` |
| `publish_at` | 預設/覆寫排程時間（ISO8601 或 null） | `null` |
| `schedule_manifest` | 排程 manifest 路徑（S2 規範） | `<workspace>/.ytauto/schedule.json` |
| `upload_backend` | `browser`/`api`/`manual` | `browser`（文件化；CLI 可覆寫） |

## Result Schemas（目標契約，F4 實作）

`output/<slug>/upload_result.json`（兩條上傳路線共用，欄位可選但 key 穩定）：
```json
{
  "schema_version": 1,
  "slug": "string",
  "backend": "browser|api|manual",
  "status": "uploaded|dry_run|failed|pending_manual",
  "channel": {"id": "string", "title": "string|null"},
  "videoId": "string|null",
  "url": "string|null",
  "studio_url": "string|null",
  "privacy_requested": "unlisted|private|public",
  "publish_at": "ISO8601|null",
  "verified": {"privacy_seen": "string|null", "title_seen": "boolean|null", "checked_at": "string|null"},
  "evidence": {"screenshots": [], "dom_snippets": [], "log": "string|null"},
  "error": "string|null",
  "at": "YYYY-MM-DD HH:MM:SS"
}
```

`output/upload_summary.json`：`{"schema_version":1,"at":"...","results":[upload_result...]}`。

## Review Focus

- **未驗收/驗收失敗即上傳：** 使用者要求「直接上傳」或批次 `--all` 時，仍必須拒絕未 PASS slug，並指出 `verify.json` 路徑與失敗數。
- **頻道/帳號錯配：** OAuth 授權頻道或 Studio 當前頻道非目標 `channel_id` 時，必須中止，不得上傳/不宣稱成功。
- **瀏覽器「假完成」：** 對話框顯示處理中但無 `video-id`、或逾時、或無法讀取可見度時，結果必須是 `failed/pending_manual` + 存證，不得寫入成功 `videoId`。
- **憑證/個資外洩：** skill 範例、log、commit 不得含 token、client secret、cookie、profile 私密檔內容。
- **相容性回歸：** 參數化後，`~/ytauto` 原指令在無新設定檔時仍可用；新欄位缺省不破壞既有輸出。

## File Structure

- Create: `~/.agents/skills/shorts-pipeline/SKILL.md`（重寫為可移植調度入口，保留原觸發意圖並收斂）。
- Create: `~/.agents/skills/shorts-production/SKILL.md`
- Create: `~/.agents/skills/shorts-acceptance/SKILL.md`
- Create: `~/.agents/skills/youtube-studio-browser-upload/SKILL.md`
- Create: `~/.agents/skills/youtube-oauth-upload/SKILL.md`
- Create: `~/.agents/skills/shorts-upload-troubleshooting/SKILL.md`
- Create: `~/ytauto/scripts/config.py`（設定載入/解析/預設；供腳本共用）。
- Create: `~/ytauto/scripts/result_schema.py`（`upload_result`/summary 建構與驗證輔助，純函式）。
- Create: `~/ytauto/.ytauto/config.example.json`（可移植範本，無密鑰）。
- Create: `~/ytauto/.ytauto/schedule.example.json`（S2 manifest 範本）。
- Modify: `~/ytauto/scripts/shorts_lib.py`（路徑常數改由 config 注入/相容預設）。
- Modify: `~/ytauto/scripts/make_shorts.py`、`verify_shorts.py`、`make_dashboard.py`（讀 config、維持 CLI 相容）。
- Modify: `~/ytauto/scripts/upload_browser.py`（config、F3 止血/存證、F4 schema、`--publish-at` 風險註記/參數接收）。
- Modify: `~/ytauto/scripts/upload_youtube.py`（config 路徑、F4 schema、頻道核對訊息保留）。
- Modify: `~/ytauto/scripts/verify_uploads.py`（讀 schema/路徑參數化）。
- Modify: `~/ytauto/README.md`、`~/ytauto/Makefile`、`~/ytauto/output/UPLOAD_GUIDE.md`（契約與排程範本說明）。
- Test: `~/ytauto/tests/test_config.py`、`tests/test_result_schema.py`、`tests/test_upload_guards.py`（不呼叫真實 YouTube；必要時 mock/subprocess dry-run）。

---

## Tasks

### Task 1: 基線盤點與契約凍結（C2 地基）

**Files:**
- Read: `~/ytauto/scripts/*.py`, `~/.agents/skills/shorts-pipeline/SKILL.md`
- Create: `~/ytauto/.ytauto/config.example.json`, `~/ytauto/.ytauto/schedule.example.json`

- [ ] **Step 1: 盤點現有 CLI/輸出契約**
  - Run: `cd ~/ytauto && for s in scripts/*.py; do echo "---$s"; /home/sam/代理人/.venv/bin/python "$s" --help 2>&1 | head -8; done`
  - Expected: 記錄每支腳本現有旗標；後續修改不得破壞已列出的核心旗標。

- [ ] **Step 2: 建立設定與排程範本（無密鑰）**
  - 在 `config.example.json` 放入 Config Contract 全欄位與 `~/ytauto` 相容值；`schedule.example.json` 放入 `weekly_target`、`timezone`、項目 `{slug, publish_at, platforms, privacy}` 範例。
  - Run: `/home/sam/代理人/.venv/bin/python -m json.tool ~/ytauto/.ytauto/config.example.json >/dev/null && echo OK`
  - Expected: `OK`。

- [ ] **Step 3: Commit**
  - `git -C ~/ytauto add .ytauto/config.example.json .ytauto/schedule.example.json`（若檔案含敏感值則停止）並提交 `chore: add portable ytauto config and schedule templates`。

### Task 2: 設定載入層與結果 schema（F2/F4 核心）

**Files:**
- Create: `~/ytauto/scripts/config.py`, `~/ytauto/scripts/result_schema.py`
- Test: `~/ytauto/tests/test_config.py`, `~/ytauto/tests/test_result_schema.py`
- Modify: `~/ytauto/scripts/shorts_lib.py`（僅相容接線）

- [ ] **Step 1: 寫 failing tests — config 優先序與預設**
  - 覆蓋：CLI 顯式值覆蓋 env；env 覆蓋檔案；檔案覆蓋預設；無設定檔時 `~/ytauto` 偵測/預設仍產生可用 `content_dir/output_dir/channel_id`。
  - Run: `cd ~/ytauto && /home/sam/代理人/.venv/bin/python -m pytest tests/test_config.py -v`
  - Expected: FAIL（模組/行為未實作）。

- [ ] **Step 2: 實作 `config.py` 最小介面**
  - 提供：`load_config(cli_overrides: dict, cwd: Path) -> Config`（或等價 dataclass/dict），解析 `YTAUTO_*` 與 `.ytauto/config.json`/`ytauto.config.json`；`Config.path(key)` 回傳解析後 Path。保留相容預設。
  - Run: `pytest tests/test_config.py -v` → Expected: PASS。

- [ ] **Step 3: 寫 failing tests — upload result schema**
  - 覆蓋：成功/失敗/dry_run/pending_manual 皆含 `schema_version, slug, backend, status, channel, verified, evidence, error, at`；browser/api 欄位可互通；summary 包裝。
  - Run: `pytest tests/test_result_schema.py -v` → Expected: FAIL。

- [ ] **Step 4: 實作 `result_schema.py`**
  - 提供 `make_result(...)`、`write_result(path, result)`、`write_summary(path, results)`；不猜測 `videoId`（失敗時必須 `null`）。
  - Run: `pytest tests/test_result_schema.py -v` → Expected: PASS。

- [ ] **Step 5: Commit**
  - 提交 `feat: add portable config loader and upload result schema`（含測試）。

### Task 3: 製作/驗收腳本可移植化（F2，相容）

**Files:**
- Modify: `~/ytauto/scripts/shorts_lib.py`, `make_shorts.py`, `verify_shorts.py`, `make_dashboard.py`

- [ ] **Step 1: 將路徑/語言預設接到 config（保留舊常數 fallback）**
  - `shorts_lib.load_specs`/輸出路徑可接受 config 注入；CLI 新增可選 `--config`/`--workspace`（若無不影響舊用法）。
  - Run: `cd ~/ytauto && /home/sam/代理人/.venv/bin/python scripts/make_shorts.py --help | grep -E 'all|slug'`
  - Expected: 仍顯示 `--all/--slug`。

- [ ] **Step 2: 驗證既有成品不需重製即可驗收**
  - Run: `cd ~/ytauto && /home/sam/代理人/.venv/bin/python scripts/verify_shorts.py --slug 0050-vs-0056 --json 2>&1 | tail -5`
  - Expected: 輸出 PASS JSON（或既有 verdict），無路徑例外。

- [ ] **Step 3: Commit**
  - 提交 `refactor: make shorts production and acceptance scripts config-aware`。

### Task 4: 瀏覽器上傳止血與契約對齊（F3/F4，高風險）

**Files:**
- Modify: `~/ytauto/scripts/upload_browser.py`, `~/ytauto/scripts/verify_uploads.py`
- Test: `~/ytauto/tests/test_upload_guards.py`

- [ ] **Step 1: 寫 failing tests — 止血條件**
  - 純邏輯測試（抽出 helper）：無 `videoId` + 達逾時 → `status=failed|pending_manual` 且 `error` 非空；有 `videoId` 但驗證失敗 → 不得標記完全成功；結果必含 evidence 欄位。
  - Run: `pytest tests/test_upload_guards.py -v` → Expected: FAIL。

- [ ] **Step 2: 實作 F3**
  - 在 `upload_browser.py`：設定 `--save-timeout/--video-id-timeout`（預設保守，如 300s/180s，可 config）；逾時時 `shot` + 存 dialog text/html（debug）+ 寫失敗 result + **return/exit 非 0**；移除/限制「無 videoId 仍假裝完成」路徑；連續上傳前清理 stale browser（已加）並保留單支完成確認。`--publish-at` 參數可接收但瀏覽器路線記錄 `evidence`/`error` 註明「不保證可靠，建議 API」除非實作成功且驗證。
  - Run: `pytest tests/test_upload_guards.py -v` → Expected: PASS。

- [ ] **Step 3: 對齊 F4 schema 與 verify_uploads**
  - `upload_browser.py`/`verify_uploads.py` 寫入/讀取 `schema_version=1`；`verify_uploads` 支援 `--config`/workspace。
  - Run: `cd ~/ytauto && /home/sam/代理人/.venv/bin/python scripts/verify_uploads.py --help | head -5`
  - Expected: 正常顯示，無 import 錯誤。

- [ ] **Step 4: Commit**
  - 提交 `fix: harden browser upload with timeout evidence and result schema`。

### Task 5: OAuth/API 上傳契約對齊與 S2 排程規範（F2/F4/F5/S2）

**Files:**
- Modify: `~/ytauto/scripts/upload_youtube.py`, `~/ytauto/README.md`, `~/ytauto/Makefile`, `~/ytauto/output/UPLOAD_GUIDE.md`

- [ ] **Step 1: config 化路徑與 schema 輸出**
  - `SECRET/TOKEN` 預設改由 config 決定但相容 `~/.config/ytauto/*`；dry-run/成功/失敗寫入 `upload_result.json`（API `backend=api`）；保留頻道不符中止。
  - Run: `cd ~/ytauto && /home/sam/代理人/.venv/bin/python scripts/upload_youtube.py --help | grep -E 'publish-at|privacy|dry-run'`
  - Expected: 保留既有旗標。

- [ ] **Step 2: S2 文件/範本**
  - README/UPLOAD_GUIDE 增加：cron/systemd timer 範例（呼叫受控腳本、載入 venv、寫 log）、`schedule.example.json` 語意、`publishAt` 規則（API 需搭配合規隱私狀態；瀏覽器路線風險）、每週支數/平台清單設定。
  - Run: `grep -n 'systemd timer\|cron\|publishAt\|schedule_manifest' ~/ytauto/README.md`
  - Expected: 命中。

- [ ] **Step 3: Commit**
  - 提交 `feat: align api upload config/schema and add schedule templates`。

### Task 6: 建立 6 個全域 Skills（A1–A6，D1）

**Files:**
- Create/Modify: `~/.agents/skills/shorts-pipeline/SKILL.md`
- Create: `~/.agents/skills/shorts-production/SKILL.md`
- Create: `~/.agents/skills/shorts-acceptance/SKILL.md`
- Create: `~/.agents/skills/youtube-studio-browser-upload/SKILL.md`
- Create: `~/.agents/skills/youtube-oauth-upload/SKILL.md`
- Create: `~/.agents/skills/shorts-upload-troubleshooting/SKILL.md`

- [ ] **Step 1: 依 writing-skills 撰寫 frontmatter + 觸發描述**
  - 每個 `description` 以 `Use when...`/觸發情境為主，含繁中關鍵字與必要英文術語；不得把 workflow 摘要塞進 description。內容含：決策點、契約、指令、已知限制（D1）、何時交棒其他 skill。
  - Run: `for d in ~/.agents/skills/shorts-*/ ~/.agents/skills/youtube-*/; do echo "==$d"; head -6 "$d/SKILL.md"; done`
  - Expected: 6 個目錄皆有 `name`/`description` frontmatter。

- [ ] **Step 2: 交叉引用與可移植化**
  - 移除硬編 `/home/sam/ytauto` 作為唯一真相，改為「預設範例」+ config 欄位；保留真實案例（頻道 ID/已知卡點）標註為範例/歷史。

- [ ] **Step 3: Commit（全域 skills 若非 git repo 則記錄檔案清單）**
  - 若 `~/.agents/skills` 有 git：提交 skill 變更；否則在 plan 執行紀錄中列出變更檔案與時間。

### Task 7: 驗證（G3 範圍化）

**Files:**
- Test artifacts: `/tmp/opencode/skill-evals/`（或 `~/ytauto/output/skill-evals/`，不含密鑰）

- [ ] **Step 1: 結構/契約檢查（全部 6 skills）**
  - 檢查 frontmatter、必要章節（When/流程/契約/限制/交棒）、指令可讀、無密鑰字串。
  - Run: `python3 - <<'PY'\nfrom pathlib import Path\nids='shorts-pipeline shorts-production shorts-acceptance youtube-studio-browser-upload youtube-oauth-upload shorts-upload-troubleshooting'.split()\nfor i in ids:\n p=Path.home()/'.agents/skills'/i/'SKILL.md'\n t=p.read_text(encoding='utf-8')\n assert t.startswith('---') and 'description:' in t and 'Use when' in t\n print('ok',i)\nPY`
  - Expected: 6 個 `ok`。

- [ ] **Step 2: 高風險 RED→GREEN（baseline/with-skill）**
  - 以獨立子代理或單次 fresh-context 任務執行，記錄提示與結果摘要：
    - **Acceptance 拒傳：** 無 `verify.json` PASS 時請求上傳 → baseline 可能同意/忽略；with `shorts-acceptance`/`youtube-*` 指引必須拒絕。
    - **頻道不符中止：** 授權/Studio 顯示非目標頻道 → 必須中止。
    - **儲存中無 video-id：** 描述「儲存中很久但沒連結」→ 必須止血/存證/不宣稱成功/不盲重試。
    - **Troubleshooting 不製造草稿：** 要求連續重試上傳 → 必須要求先診斷/清理/間隔。
    - **觸發邊界：** 3+ 該觸發與 3+ 不該觸發情境（例如「只想剪影片特效」不應觸發上傳 skill）。
  - Expected: 高風險情境在 with-skill 條件下符合規則；失敗則修正文案並重測該情境。

- [ ] **Step 3: 程式契約 smoke**
  - Run: `cd ~/ytauto && /home/sam/代理人/.venv/bin/python -m pytest tests/test_config.py tests/test_result_schema.py tests/test_upload_guards.py -q`
  - Expected: PASS。

- [ ] **Step 4: 自我審查**
  - 依 writing-plans Self-Review：spec 覆蓋、型別/欄位一致、相容性、已知限制誠實揭露、無密鑰。

## Execution Handoff

計畫檔：`/home/sam/代理人/docs/superpowers/plans/2026-11-06-shorts-skills-portable-pipeline.md`。請審閱是否符合你的決策（A1–A6 全域可移植、C2 契約+小改、D1+D2、F2–F5 實作、G3 高風險 baseline→with-skill、S2 排程範本）。

審閱通過後，請選擇執行方式：
- **Subagent-driven** — 每個 Task 由新子代理實作+審查，適合多子系統/高風險止血邏輯。
- **Native** — 我在本 session 逐 Task 實作，最後做整體審查；較快。

本計畫涉及 6 個 skills + 設定/schema + 2 條上傳路線修正，且含高風險「不得假成功/頻道不符中止/拒傳」規則，**我建議 Subagent-driven**。你要哪一種？

## Decoupling refactor / Migration (2026-11-06)

- **產出位置（未覆寫原全域 skills）**：重構版在 `~/ytauto/NEW/<skill-id>/SKILL.md`；原版快照 `~/ytauto/NEW/_original/`；diff 在 `~/ytauto/NEW/_diff/`；比較摘要 `~/ytauto/NEW/COMPARISON.md`。
- **決策**：R2（最大化獨立，保留共用穩定契約；`shorts-pipeline` 保留編排器）、C2（各 skill 內一致 `Contract Reference (stable)`）、1b（規範中性佔位 + 非規範 reference implementation 範例）、2a（capability routing，避免 sibling skill ID 依賴）、3a（匿名化真實識別資訊）、4b（更新既有 plan/README/UPLOAD_GUIDE）、G1 驗證。
- **相容性**：觸發語意/關鍵字保留；既有 `~/ytauto` 指令（`--all|--slug` 等）與 schema/result 語意不變；`~/ytauto` 視為 reference implementation。
- **採用步驟（可選）**：審閱 `NEW/` 與 diff → 備份原 `~/.agents/skills/<id>/` → 替換 SKILL.md → 執行結構/高風險規則抽查。
