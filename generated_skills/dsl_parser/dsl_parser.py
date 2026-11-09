"""DSL Parser Skill：封裝 csv2ast 與 疊構解析。"""
import sys
sys.path.insert(0, "/home/sam/代理人")
from 疊構Util import csv2ast, 疊構解析


class DSLParserSkill:
    def csv_to_ast(self, df):
        # TODO: AI 推論部分 - DataFrame 欄位驗證
        return csv2ast(df)

    def parse(self, ast):
        # TODO: AI 推論部分 - AST 結構驗證
        return 疊構解析(ast)