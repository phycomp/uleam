"""驗收報告產生器：JSON + Markdown 雙輸出。"""

import json
import os
from typing import Any, Dict


class AcceptanceReportGenerator:
    def generate(self, report: Any, output_path: str) -> Dict[str, str]:
        base = output_path
        os.makedirs(os.path.dirname(base) or ".", exist_ok=True)
        json_path = base + ".json"
        md_path = base + ".md"
        data = {
            "started_at": getattr(report, "started_at", ""),
            "finished_at": getattr(report, "finished_at", ""),
            "overall_pass": getattr(report, "overall_pass", None),
            "summary": getattr(report, "summary", {}),
            "stages": [
                {
                    "stage_id": getattr(s, "stage_id", None),
                    "name": getattr(s, "name", None),
                    "status": getattr(s, "status", None),
                    "kpi_checks": getattr(s, "kpi_checks", []),
                    "errors": getattr(s, "errors", []),
                }
                for s in (getattr(report, "stages", []) or [])
            ],
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # markdown
        lines = [
            "# 驗收報告",
            "",
            f"- 整體：{'PASS' if data['overall_pass'] else 'FAIL'}",
            f"- 階段數：{len(data['stages'])}",
            "",
        ]
        for st in data["stages"]:
            lines.append(f"## Stage {st['stage_id']} {st['name']} — {st['status']}")
            for kc in st["kpi_checks"]:
                lines.append(f"- {kc}")
            if st["errors"]:
                for e in st["errors"]:
                    lines.append(f"  - ERROR: {e}")
            lines.append("")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return {"json": json_path, "md": md_path}


__all__ = ["AcceptanceReportGenerator"]
