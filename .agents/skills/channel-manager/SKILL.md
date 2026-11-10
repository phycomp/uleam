---
name: channel-manager
description: "頻道管理技能：列出頻道/播放清單、建立播放清單、加入視頻、crontab 排程、內容主題模板（quantum/sciedu/PQC）。Use when the user wants to manage YouTube channels, create playlists, schedule content, or set up content calendar."
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---
# Channel Manager — 頻道管理

## 功能
- `列出頻道()`：列出所有頻道。
- `列出播放清單()`：列出所有播放清單。
- `建立播放清單(title, desc, privacy)`：建立播放清單。
- `加入視頻(playlist_id, video_id)`：加入視頻。
- `crontab_template()`：每週 2 支短視頻 + 1 支長視頻排程。

## 內容主題模板
- `content_templates/quantum.md`：量子傳輸線
- `content_templates/sciedu.md`：科學教育
- `content_templates/pqc.md`：後量子密碼

## 使用
```bash
cd /home/sam/代理人
python -c "
import sys; sys.path.insert(0,'.')
from 頻道管理 import 列出頻道, 列出播放清單, 建立播放清單, crontab_template
print(列出頻道())
print(列出播放清單())
"
```

## 觸發條件
- 「頻道管理」「channel manager」「播放清單」「crontab」「內容排程」「quantum/sciedu/PQC」
