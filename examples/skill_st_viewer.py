from streamlit import expander, json as stJson, markdown, set_page_config, sidebar, subheader, title, write, radio
from sys import path
"""Streamlit 版 Skill Viewer：側邊欄列出所有上層級，點選後以 JSON 顯示下層級。"""

import json
import os
import sys

import streamlit as st

path.insert(0, "/home/sam/代理人")
from examples.skill_viewer import HIERARCHY, load_skills, parse_frontmatter

set_page_config(page_title="Skill Viewer", layout="wide")
title("Skill Hierarchy Viewer")

skills = load_skills()
skill_map = {s["name"]: s for s in skills}

with sidebar:
# 側邊欄：上層級清單
  parents = sorted(HIERARCHY.keys())
  selected = radio("選擇上層級技能", parents)

  # markdown("---")
  write(f'共{len(parents)}類別')
  write(f"共 {len(skills)} 個技能")

# 主區：JSON 輸出
if selected:
    children = HIERARCHY.get(selected, [])
    out = {"parent": selected, "children": []}
    for c in children:
        if c in skill_map:
            info = dict(skill_map[c])
            info["installed"] = True
            out["children"].append(info)
        else:
            out["children"].append({"name": c, "installed": False})
    subheader(f"上層級：{selected}")
    write(f"下層級數量：{len(children)}")
    stJson(out)

    # 額外：顯示每個子技能的詳細資訊
    markdown("---")
    subheader("子技能詳細")
    for c in children:
        if c in skill_map:
            info = skill_map[c]
            with expander(c):
                write(f"**來源**: {info['source']}")
                write(f"**Usage**: {info['desc']}")
                write(f"**作者**: {info['author'] or '(未指定)'}")
                write(f"**版本**: {info['version'] or '(未指定)'}")
                write(f"**工具**: {info['usage'] or '(未指定)'}")
                write(f"**備註**: {info['notes'] or '(無)'}")
