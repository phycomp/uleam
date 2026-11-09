"""Greeter Skill 範本：示範 skill-generator 產出結構。"""
from typing import List


class Greeter:
    def __init__(self, prefix: str = "Hello"):
        # TODO: AI 推論部分 - prefix 驗證與多語系支援
        self.prefix = prefix

    def greet(self, name: str) -> str:
        # TODO: AI 推論部分 - 名稱清理與空值處理
        return f"{self.prefix}, {name}!"

    def greet_many(self, names: List[str]) -> List[str]:
        return [self.greet(n) for n in names]