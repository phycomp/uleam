"""Agent Workflow Skill：封裝 代理主程式 狀態機。"""
import sys
sys.path.insert(0, "/home/sam/代理人")
from 代理主程式 import run_workflow


class AgentWorkflowSkill:
    def __init__(self, max_iter: int = 10):
        # TODO: AI 推論部分 - 初始狀態建構與參數驗證
        self.max_iter = max_iter

    def run(self, initial_state: dict):
        # TODO: AI 推論部分 - 狀態深拷貝與結果篩選
        return run_workflow(initial_state, max_iter=self.max_iter)