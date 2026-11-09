"""驗收 pipeline 編排器。"""

import json
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

ROOT = "/home/sam/代理人"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from .stages import PipelineContext, build_stages, StageResult


@dataclass
class PipelineReport:
    started_at: str = ""
    finished_at: str = ""
    stages: List[StageResult] = field(default_factory=list)
    overall_pass: bool = False
    summary: Dict[str, Any] = field(default_factory=dict)


class AcceptancePipeline:
    def __init__(self, root: str = ROOT, output_dir: Optional[str] = None):
        self.root = root
        self.output_dir = output_dir or os.path.join(root, "acceptance_output")

    def run(
        self, ctx: Optional[PipelineContext] = None, stages: Optional[List[int]] = None
    ) -> PipelineReport:
        if ctx is None:
            ctx = PipelineContext(root=self.root, output_dir=self.output_dir)
        all_stages = build_stages()
        if stages is not None:
            all_stages = [s for s in all_stages if s.stage_id in stages]
        report = PipelineReport(started_at=time.strftime("%Y-%m-%dT%H:%M:%S"))
        for st in all_stages:
            sr = st.run(ctx)
            ctx.stage_results.append(sr)
            report.stages.append(sr)
        report.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        report.overall_pass = all(
            s.status in ("pass", "skipped") for s in report.stages
        )
        report.summary = {
            "stage_count": len(report.stages),
            "passed": sum(1 for s in report.stages if s.status == "pass"),
            "failed": sum(1 for s in report.stages if s.status == "fail"),
            "skipped": sum(1 for s in report.stages if s.status == "skipped"),
        }
        os.makedirs(self.output_dir, exist_ok=True)
        try:
            with open(
                os.path.join(self.output_dir, "acceptance_report.json"),
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(
                    {
                        "started_at": report.started_at,
                        "finished_at": report.finished_at,
                        "overall_pass": report.overall_pass,
                        "summary": report.summary,
                        "stages": [
                            {
                                "stage_id": s.stage_id,
                                "name": s.name,
                                "status": s.status,
                                "kpi_checks": s.kpi_checks,
                                "errors": s.errors,
                                "duration_s": s.duration_s,
                            }
                            for s in report.stages
                        ],
                    },
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
        except Exception:
            pass
        return report


__all__ = ["AcceptancePipeline", "PipelineReport"]
