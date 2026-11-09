import sys, importlib.util
sys.path.insert(0, "/home/sam/代理人")
spec = importlib.util.spec_from_file_location("aw", "/home/sam/代理人/generated_skills/agent_workflow/agent_workflow.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
AWS = m.AgentWorkflowSkill

def test_run():
    state = {
        "target_zo": 50.0, "frequency_ghz": 6.0, "temperature_profile": [],
        "current_stackup": [], "is_symmetric": True, "electrical_results": {},
        "thermal_results": {}, "coherence_score": 0.0, "iteration_count": 0,
        "solution_pool": [],
    }
    r = AWS(max_iter=2).run(state)
    assert "iteration_count" in r
    assert r["iteration_count"] >= 1