30 08 * * 1 docker run --rm quantum-agent:v1 '{"target_zo": 50.0, "thermal_budget_uw": 1.0, "min_h_mil": 4.0, "er_dielectric": 4.2}' >> /var/log/quantum_agent.log 2>&1
