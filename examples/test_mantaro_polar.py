"""測試 mantaro 與 polar 技能。"""
import subprocess, sys, os

# 1. Mantaro: 驗證來源頁面可編譯
print("=== Mantaro ===")
r = subprocess.run(["/home/sam/flex/bin/python", "-m", "py_compile",
                    "/home/sam/量傳線/德夫/pages/26Mantaro風格.py"],
                   capture_output=True, text=True)
print("compile:", "PASS" if r.returncode == 0 else "FAIL")
if r.returncode != 0:
    print(r.stderr)

# 2. Polar: 執行採樣計畫
print("=== Polar ===")
r = subprocess.run(["/home/sam/opencode/revphy/.venv/bin/python",
                    "/home/sam/opencode/revphy/tools/polar_sampling_plan.py"],
                   capture_output=True, text=True,
                   env={**os.environ, "PYTHONPATH": "/home/sam/opencode/revphy/src"})
print(r.stdout.strip().splitlines()[-3:] if r.stdout else "")
print("exit:", r.returncode)
assert r.returncode == 0, r.stderr
print("Polar: PASS")
