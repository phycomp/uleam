"""pytest 編排器。"""

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List

ROOT = "/home/sam/代理人"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@dataclass
class TestReport:
    status: str = "skipped"  # pass / fail / skipped / error
    exit_code: int = -1
    stdout: str = ""
    stderr: str = ""
    passed: int = 0
    failed: int = 0
    tests: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "exit_code": self.exit_code,
            "passed": self.passed,
            "failed": self.failed,
            "tests": self.tests,
            "stdout": self.stdout[:2000],
            "stderr": self.stderr[:2000],
        }


class TestRunner:
    def __init__(self, root: str = ROOT):
        self.root = root

    def _pytest_bin(self) -> str:
        w = shutil.which("pytest")
        if w:
            return w
        cand = "/home/sam/opencode/revphy/.venv/bin/pytest"
        if os.path.exists(cand):
            return cand
        return ""

    def _pytest_available(self) -> bool:
        return bool(self._pytest_bin())

    def _run_pytest(self, args: List[str]) -> TestReport:
        rep = TestReport()
        if os.environ.get("PYTEST_CURRENT_TEST"):
            rep.status = "skipped"
            rep.stderr = "running under pytest; skipped to avoid recursion"
            return rep
        binp = self._pytest_bin()
        if not binp:
            rep.status = "skipped"
            rep.stderr = "pytest not found"
            return rep
        try:
            proc = subprocess.run(
                [binp] + args,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=300,
            )
            rep.exit_code = proc.returncode
            rep.stdout = proc.stdout
            rep.stderr = proc.stderr
            import re

            m = re.search(r"(\d+) passed", proc.stdout)
            if m:
                rep.passed = int(m.group(1))
            m = re.search(r"(\d+) failed", proc.stdout)
            if m:
                rep.failed = int(m.group(1))
            rep.status = "pass" if proc.returncode == 0 else "fail"
        except Exception as e:
            rep.status = "error"
            rep.stderr = str(e)
        return rep

    def run_unit(self, paths: List[str] = None) -> TestReport:
        args = ["-q"]
        if paths:
            args = args + paths
        return self._run_pytest(args)

    def run_integration(self) -> TestReport:
        return self._run_pytest(["-q", "tests/"])

    def run_acceptance(self) -> TestReport:
        return self._run_pytest(["-q", "tests/test_acceptance_pipeline.py"])

    def run_all(self) -> TestReport:
        return self._run_pytest(["-q", "tests/"])


__all__ = ["TestRunner", "TestReport"]
