---
name: txt-proc
description: "文件轉換 pipeline 技能：純文字 → Markdown → PPTX，含 compact 合併、主題 (dark/light/tech/warm + genoffice dark_tech 等)、font-size 自動調整、genoffice CLI 轉換、測試。Use when the user wants to convert text to markdown to pptx, create slides from text, or build a text-to-presentation pipeline."
version: "1.2.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---
# txt-proc — 文件轉換 Pipeline (text → md → pptx)

## Python 實作（不需 build）
- `pipeline/text_to_md.py`：`text_to_md()`、`md_to_slides()`
- `pipeline/md_to_pptx.py`：`md_to_pptx(md, out_path)`（python-pptx）
- `pipeline_cli.py`：CLI 入口（python-pptx）

## GenOffice CLI 轉換
- `genoffice_convert.py`：GenOffice CLI 轉換（genoffice create --ops），含 compact/theme
```bash
cd ~/genoffice
python genoffice_convert.py input.txt --out output.pptx --compact --theme dark
```

## 主題 (theme)
- basic (python-pptx): light / dark / tech / warm
- advanced (genoffice): dark / light / tech / warm / dark_tech / corporate_blue / emerald_nature / warm_warmth

## Compact 模式
- `--compact`：合併短內容投影片（最多 3 個）。
- 合併時標題自動摘要（>40 字元截斷 + "等 N 項"）。
- font-size 自動調整避免 overflow。

## 使用
```bash
cd ~/genoffice
python pipeline_cli.py input.txt --out output.pptx --md output.md --compact --theme dark
python genoffice_convert.py input.txt --out output.pptx --compact --theme dark
```

## 測試
```bash
cd ~/genoffice
python test_pipeline.py
python test_genoffice_convert.py
```

## 觸發條件
- 「text to pptx」「文字轉投影片」「markdown 轉 pptx」「text→md→pptx」「genoffice」