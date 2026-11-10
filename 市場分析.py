"""視頻市場分析模組。"""


def 推薦上傳頻率(平台: str = "youtube") -> dict:
    freq = {
        "youtube_shorts": {"shorts_per_week": 2, "long_per_week": 1},
        "tiktok": {"shorts_per_week": 3, "long_per_week": 0},
        "instagram_reels": {"shorts_per_week": 2, "long_per_week": 0},
    }
    return freq.get(平台, freq["youtube_shorts"])


def 主題比較(主題列表: list) -> list:
    """依競爭度/成長潛力/製作難度排序主題。"""
    # 簡化：回傳原始列表，實際可擴充評分
    return 主題列表


def crontab_視頻排程():
    return """# 每週 2 支短視頻 + 1 支長視頻
0 12 * * 2,5 cd /home/sam/ytauto && python scripts/make_shorts.py --all
0 10 * * 0 cd /home/sam/Oloid && python scripts/render_matplotlib.py models/oloid.stl renders && ffmpeg -y -framerate 30 -i renders/frame_%04d.png -c:v libx264 -pix_fmt yuv420p video_weekly.mp4
"""
