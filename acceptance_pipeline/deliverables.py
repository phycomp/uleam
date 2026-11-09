"""交付打包器：收集 artifacts 並產生 MANIFEST.json。"""

import hashlib
import json
import os
import shutil
from typing import Any, Dict, List


class DeliverablePackager:
    def package(
        self, output_dir: str, artifacts: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)
        manifest = {"files": [], "timestamp": None}
        import datetime

        manifest["timestamp"] = datetime.datetime.now().isoformat()
        for category, paths in (artifacts or {}).items():
            for p in paths or []:
                src = p if os.path.isabs(p) else os.path.join("/home/sam/代理人", p)
                if not os.path.exists(src):
                    manifest["files"].append(
                        {"path": p, "category": category, "status": "missing"}
                    )
                    continue
                dst = os.path.join(
                    output_dir, "deliverables", category, os.path.basename(p)
                )
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                try:
                    shutil.copy2(src, dst)
                    with open(src, "rb") as f:
                        sha = hashlib.sha256(f.read()).hexdigest()
                    manifest["files"].append(
                        {
                            "path": p,
                            "category": category,
                            "status": "ok",
                            "sha256": sha,
                            "dest": dst,
                        }
                    )
                except Exception as e:
                    manifest["files"].append(
                        {"path": p, "category": category, "status": f"error: {e}"}
                    )
        manifest_path = os.path.join(output_dir, "MANIFEST.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        manifest["manifest_path"] = manifest_path
        return manifest


__all__ = ["DeliverablePackager"]
