"""頻道管理模組：列出頻道、分類視頻、crontab 排程。"""

import json
import sys

sys.path.insert(0, "/home/sam/ytauto/scripts")
import upload_youtube as u
from googleapiclient.discovery import build

CHANNELS = {
    "invest": {
        "name": "投資短影音",
        "handle": "@investshorts",
        "id": "UCGQja3bvv7PBxuZjqnC7Wkg",
    },
    "3dprint": {"name": "3D 列印產品", "handle": "@3dprint", "id": None},
    "quantum": {"name": "量子傳輸線", "handle": "@quantumtline", "id": None},
    "sciedu": {"name": "科學教育", "handle": "@sciedu", "id": None},
    "pqc": {"name": "後量子密碼", "handle": "@pqc", "id": None},
}

PLAYLISTS = {
    "oloid": "Oloid 3D 列印產品",
    "ai": "AI",
    "wealth": "致富",
    "quantum": "量子傳輸線",
    "sciedu": "科學教育",
    "pqc": "後量子密碼",
}


def 列出頻道():
    yt = build(
        "youtube",
        "v3",
        credentials=u.credentials(token_path=u._TOKEN),
        cache_discovery=False,
    )
    ch = yt.channels().list(part="snippet,statistics", mine=True).execute()
    return ch.get("items", [])


def 列出播放清單():
    yt = build(
        "youtube",
        "v3",
        credentials=u.credentials(token_path=u._TOKEN),
        cache_discovery=False,
    )
    pl = yt.playlists().list(part="snippet", mine=True, maxResults=50).execute()
    return pl.get("items", [])


def 建立播放清單(title, description="", privacy="public"):
    yt = build(
        "youtube",
        "v3",
        credentials=u.credentials(token_path=u._TOKEN),
        cache_discovery=False,
    )
    pl = (
        yt.playlists()
        .insert(
            part="snippet,status",
            body={
                "snippet": {"title": title, "description": description},
                "status": {"privacyStatus": privacy},
            },
        )
        .execute()
    )
    return pl


def 加入視頻(playlist_id, video_id):
    yt = build(
        "youtube",
        "v3",
        credentials=u.credentials(token_path=u._TOKEN),
        cache_discovery=False,
    )
    yt.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    ).execute()
    return True


def crontab_template():
    return """# 每週 2 支短視頻 + 1 支長視頻
# 短視頻：週二、週五 12:00
0 12 * * 2,5 cd /home/sam/ytauto && /home/sam/flex/bin/python scripts/make_shorts.py --all
# 長視頻：週日 10:00
0 10 * * 0 cd /home/sam/Oloid && /home/sam/flex/bin/python scripts/render_matplotlib.py models/oloid.stl renders && ffmpeg -y -framerate 30 -i renders/frame_%04d.png -c:v libx264 -pix_fmt yuv420p video_weekly.mp4
"""
