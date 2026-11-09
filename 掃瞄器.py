import ast
import os
import json

class RepoASTScanner(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path
        self.features = {"classes": [], "functions": []}

    def visit_ClassDef(self, node):
        class_info = {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "methods": []
        }
        # 掃描類別內部的函數
        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef):
                class_info["methods"].append(self._parse_function(body_item))
        self.features["classes"].append(class_info)

    def visit_FunctionDef(self, node):
        # 頂層函數（非類別內部的函數）
        self.features["functions"].append(self._parse_function(node))

    def _parse_function(self, node):
        return {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "args": [arg.arg for arg in node.args.args],
            "returns": ast.unparse(node.returns) if node.returns else "None"
        }

def scan_repo(repo_path):
    repo_summary = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_path)
                
                with open(full_path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file)
                        scanner = RepoASTScanner(rel_path)
                        scanner.visit(tree)
                        # 只有當檔案內有定義 class 或 function 時才記錄
                        if scanner.features["classes"] or scanner.features["functions"]:
                            repo_summary[rel_path] = scanner.features
                    except SyntaxError:
                        continue # 略過語法有誤的檔案
    return repo_summary

# 測試掃描（可替換為你的 repo 路徑）
if __name__ == "__main__":
    # repo_data = scan_repo("./my_agent_repo")
    # print(json.dumps(repo_data, indent=2, ensure_ascii=False))
    pass
