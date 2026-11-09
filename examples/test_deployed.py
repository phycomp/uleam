"""部署測試：測試已佈署的 Cloudflare 服務。"""

import sys
import urllib.request
import urllib.error


def test_health(base_url: str) -> bool:
    url = base_url.rstrip("/") + "/_stcore/health"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            print(f"Health check: {resp.status} {resp.read().decode()[:100]}")
            return resp.status == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False


def test_home(base_url: str) -> bool:
    url = base_url.rstrip("/") + "/"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            print(f"Home page: {resp.status}, length={len(resp.read())}")
            return resp.status == 200
    except Exception as e:
        print(f"Home page failed: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_deployed.py <base_url>")
        sys.exit(1)
    base = sys.argv[1]
    ok1 = test_home(base)
    ok2 = test_health(base)
    print("RESULT:", "PASS" if (ok1 and ok2) else "FAIL")
    sys.exit(0 if (ok1 and ok2) else 1)
