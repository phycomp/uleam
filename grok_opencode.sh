#!/usr/bin/env bash
# grok_opencode.sh — grok-build + opencode LLM 使用/測試腳本
set -u

GROK="${GROK_BIN:-grok}"
PASS=0
FAIL=0

run_test() {
  local name="$1"; shift
  local expected="$1"; shift
  echo "=== $name ==="
  local out
  out=$(timeout 120 "$GROK" "$@" 2>&1)
  local rc=$?
  echo "$out"
  if [ $rc -ne 0 ]; then
    echo "[FAIL] exit=$rc"
    FAIL=$((FAIL+1))
    return
  fi
  if echo "$out" | grep -q "$expected"; then
    echo "[PASS]"
    PASS=$((PASS+1))
  else
    echo "[FAIL] expected '$expected' not found"
    FAIL=$((FAIL+1))
  fi
}

echo "### grok version ###"
"$GROK" --version

echo "### model list ###"
"$GROK" models

# Test 1: beam-free (should succeed)
run_test "Beam Free inference" "OK" -p "reply with exactly: OK" -m opencode-beam-free

# Test 2: beam-free longer prompt
run_test "Beam Free summarize" "summary" -p "Reply with one word: summary" -m opencode-beam-free

# Test 3: big-pickle connectivity (via direct curl; grok retries on 429 and may hang)
echo "=== Big Pickle connectivity (direct curl) ==="
KEY="oc_sk_2ec02e175c00_yTQjxkTcULLJljrM_THGejclwP4C8OMH"
ORG="org_01M63D7WQPNQJ7MC7Z318WPJD3"
RESP=$(curl -s -m 30 https://opencode.ai/inference/openai/v1/chat/completions \
  -H "Authorization: Bearer $KEY" -H "x-opencode-org-id: $ORG" -H "Content-Type: application/json" \
  -d '{"model":"big-pickle","messages":[{"role":"user","content":"reply OK"}],"max_tokens":10}')
echo "$RESP"
if echo "$RESP" | grep -q "FreeUsageLimitError"; then
  echo "[SKIP] big-pickle rate-limited (daily free quota exhausted) — config still valid"
elif echo "$RESP" | grep -q '"choices"'; then
  echo "[PASS] big-pickle reachable"
  PASS=$((PASS+1))
else
  echo "[FAIL] unexpected response"
  FAIL=$((FAIL+1))
fi

echo ""
echo "=============================="
echo "PASS=$PASS  FAIL=$FAIL"
echo "=============================="

if [ $FAIL -gt 0 ]; then exit 1; fi
exit 0
