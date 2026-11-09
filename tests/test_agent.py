import os
os.environ.setdefault("MAX_ITERATIONS", "4")
os.environ.setdefault("SOLUTION_POOL_TARGET", "2")

def test_tools():
    from agent_system.tools import calc_impedance_and_loss, make_stackup, check_drc
    r = calc_impedance_and_loss(10.0, 5.5, "NbTi", 8.0)
    assert 40 <= r["Zo"] <= 60, r
    s = make_stackup("NbTi", 10.0, 5.5)
    d = check_drc(s)
    assert d["ok"], d
    print("test_tools PASS")

def test_llm():
    from agent_system.llm import chat
    out = chat("Reply only OK.", "ping")
    assert isinstance(out, str)
    print("test_llm PASS:", out[:40])

def test_graph():
    from agent_system.graph import run
    r = run({"target_zo": 50.0, "freq": 8.0, "min_thickness": 4.0}, thread_id="t")
    assert r.get("status") == "done"
    assert len(r.get("solution_pool", [])) >= 1
    print("test_graph PASS: pool=", len(r["solution_pool"]))

if __name__ == "__main__":
    test_tools()
    test_llm()
    test_graph()
    print("ALL AGENT TESTS PASS")
