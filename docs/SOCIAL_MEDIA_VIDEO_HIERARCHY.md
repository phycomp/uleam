# Social Media / Video Production 技能層級 (Hierarchy)

## 主技能 (Primary)
| 技能 | 說明 |
|------|------|
| video | 通用影片製作（AI + 程式化） |
| social | 社群媒體內容（LinkedIn/Twitter/IG/TikTok/FB） |
| hyperframes | HyperFrames 影片渲染（HTML→video） |
| remotion | Remotion 影片（React） |
| shorts-pipeline | Shorts 全流程（選題→製作→驗收→上傳） |

## 次技能 (Secondary) — 視頻製作
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| create-video | video | HeyGen Video Agent 提示式生成 |
| avatar-video | video | AI avatar 精確控制 |
| ai-video-gen | video | 多提供者 AI 視頻生成 |
| video-edit | video | ffmpeg 本地剪輯 |
| video-understand | video | ffmpeg+Whisper 理解視頻 |
| video-download | video | yt-dlp 下載 |
| video-translate | video | HeyGen 翻譯/配音 |
| video-toolkit | video | claude-code-video-toolkit |
| hyperframes-* | hyperframes | animation/core/cli/media/registry/creative |
| remotion-* | remotion | captions/create/docs/render/studio 等 |
| motion-graphics | video | 動態圖形 |
| create-video | video | 提示式視頻生成 |

## 次技能 — 音訊/媒體
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| elevenlabs | media | TTS/音效/音樂 |
| acestep | media | AI 音樂生成 |
| music | media | ElevenLabs Music |
| sound-effects | media | 音效生成 |
| speech-to-text | media | 轉錄 |
| tts (text-to-speech) | media | TTS |
| media-use | media | Agent Media OS |

## 次技能 — 社群媒體
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| social-publisher | social | 多平台發布 |
| tiktok-marketing | social | TikTok 策略 |
| twitter-x-automation | social | Twitter/X 自動化 |
| linkedin-automation | social | LinkedIn 自動化 |
| facebook-meta-ads | social | Meta 廣告 |
| instagram (via social) | social | IG 內容 |
| community-marketing | social | 社群行銷 |
| influencer-marketing | social | 網紅行銷 |
| email-marketing | social | 郵件行銷 |
| sms | social | SMS 行銷 |

## 次技能 — YouTube
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| YouTube Automation | social | 頻道管理 |
| youtube-oauth-upload | social | OAuth 上傳 |
| youtube-studio-browser-upload | social | Studio 瀏覽器上傳 |
| shorts-pipeline | social+video | Shorts 全流程 |
| shorts-production | shorts-pipeline | 製作 |
| shorts-acceptance | shorts-pipeline | 驗收 |
| shorts-upload-troubleshooting | shorts-pipeline | 上傳診斷 |
| youtube-oauth-upload | shorts-pipeline | API 上傳 |

## 次技能 — 內容與文案
| 技能 | 主依賴 | 說明 |
|------|--------|------|
| copywriting | content | 行銷文案 |
| copy-editing | copywriting | 文案編輯 |
| content-strategy | content | 內容策略 |
| content-research-writer | content | 內容研究寫作 |
| ads-copywriter | content | 廣告文案 |
| ad-creative | content | 廣告創意 |

## 依賴關係圖
```
video (核心)
├── create-video, avatar-video, ai-video-gen
├── video-edit, video-understand, video-download, video-translate
├── hyperframes → hyperframes-* (animation, core, cli, media, creative, registry)
├── remotion → remotion-* (captions, create, docs, render, studio, ...)
├── motion-graphics
└── video-toolkit

social (核心)
├── social-publisher
├── tiktok-marketing, twitter-x-automation, linkedin-automation
├── facebook-meta-ads, community-marketing, influencer-marketing
├── email-marketing, sms
└── YouTube Automation → youtube-oauth-upload, youtube-studio-browser-upload
    └── shorts-pipeline → shorts-production, shorts-acceptance, shorts-upload-troubleshooting

media (核心)
├── elevenlabs, acestep, music, sound-effects
├── speech-to-text, text-to-speech, media-use
└── (feeds into video)

content (核心)
├── copywriting → copy-editing
├── content-strategy, content-research-writer
├── ads-copywriter, ad-creative
└── (feeds into social/video)
```