#!/usr/bin/env bash
set -u
cd /home/sam/代理人/量子傳輸線測試
PY=/home/sam/代理人/.venv/bin/python
PASS=0; FAIL=0

if $PY run_scenarios.py > /tmp/opencode/qts.log 2>&1; then
  echo "[PASS] run_scenarios.py exited 0"; PASS=$((PASS+1))
else
  echo "[FAIL] run_scenarios.py"; FAIL=$((FAIL+1))
fi
echo "--- tail ---"; tail -6 /tmp/opencode/qts.log
if grep -q "Saved results.json" /tmp/opencode/qts.log; then echo "[PASS] results.json saved"; PASS=$((PASS+1)); else echo "[FAIL]"; FAIL=$((FAIL+1)); fi
if [ -s results.json ]; then echo "[PASS] results.json non-empty"; PASS=$((PASS+1)); else echo "[FAIL]"; FAIL=$((FAIL+1)); fi
echo "PASS=$PASS FAIL=$FAIL"
[ $FAIL -eq 0 ]
