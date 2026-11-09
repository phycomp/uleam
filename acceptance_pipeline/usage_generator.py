"""使用說明產生器：自動產生 markdown 使用說明。"""

import os
from typing import Any


class UsageGenerator:
    def generate(self, output_path: str, pipeline_report: Any = None) -> str:
        stages = []
        overall = True
        if pipeline_report is not None:
            stages = getattr(pipeline_report, "stages", []) or []
            overall = getattr(pipeline_report, "overall_pass", True)
        lines = []
        lines.append("# 量子傳輸線驗收 Pipeline 使用說明")
        lines.append("")
        lines.append("## 安裝")
        lines.append("```bash")
        lines.append("cd /home/sam/代理人")
        lines.append("pip install -r requirements.txt")
        lines.append("```")
        lines.append("")
        lines.append("## 執行")
        lines.append("```bash")
        lines.append(
            'python -c "from acceptance_pipeline.pipeline import AcceptancePipeline; print(AcceptancePipeline().run().overall_pass)"'
        )
        lines.append("```")
        lines.append("")
        lines.append("## 測試")
        lines.append("```bash")
        lines.append("pytest tests/test_acceptance_pipeline.py -v")
        lines.append("```")
        lines.append("")
        lines.append("## KPI 驗收結果")
        lines.append(f"- 整體通過：{'YES' if overall else 'NO'}")
        lines.append(f"- 階段數：{len(stages)}")
        for s in stages:
            sid = getattr(s, "stage_id", "?")
            name = getattr(s, "name", "?")
            status = getattr(s, "status", "?")
            lines.append(f"  - Stage {sid} {name}: {status}")
        lines.append("")
        lines.append("## 材料數據庫")
        lines.append(
            "資料位於 `acceptance_pipeline/materials.json`，API：`MaterialDB`。"
        )
        lines.append("")
        lines.append("## 交付物")
        lines.append("- 程式碼：acceptance_pipeline/")
        lines.append("- 測試：tests/test_acceptance_pipeline.py")
        lines.append("- 驗收標準：acceptance_pipeline/acceptance_criteria.yaml")
        lines.append("- 報告：acceptance_output/acceptance_report.json")
        lines.append("")
        md = "\n".join(lines)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md)
        return md


__all__ = ["UsageGenerator"]
