# 建立圖結構
workflow.add_node("Init", init_design_node)
workflow.add_node("ElecCalc", electrical_calc_node)
workflow.add_node("ThermalCalc", thermal_calc_node)
workflow.add_node("Review", quantum_coherence_review_node)
workflow.add_node("Generator", solution_generator_node)

workflow.set_entry_point("Init")
workflow.add_edge("Init", "ElecCalc")
workflow.add_edge("ElecCalc", "ThermalCalc")
workflow.add_edge("ThermalCalc", "Review")
# 根據狀態決定是要繼續優化，還是產出報告
workflow.add_conditional_edges(
    "Review",
    should_continue,
    {
        "generate_final": "Generator",
        "loop_optimize": "ElecCalc" # 回到計算節點重新跑模擬
    }
)
workflow.add_edge("Generator", END)
app = workflow.compile()
