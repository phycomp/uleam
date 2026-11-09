#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/sam/代理人"
export PYTHONPATH="${ROOT}:${PYTHONPATH:-}"
cd "$ROOT"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

if $DRY_RUN; then
  echo "[dry-run] PYTHONPATH=$PYTHONPATH"
  python -c "import acceptance_pipeline; print('import ok')"
  exit 0
fi

echo "=== Running pytest ==="
pytest tests/test_acceptance_pipeline.py -q || true

echo "=== Running acceptance pipeline ==="
python -c "from acceptance_pipeline.pipeline import AcceptancePipeline; r=AcceptancePipeline().run(); print('overall_pass=', r.overall_pass)"

echo "=== Done ==="