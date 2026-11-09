import os
import json
import argparse
import sys
from openai import OpenAI

# 假設我們先前寫好的 AST 掃描器存在於同目錄的 ast_scanner.py 中
# 如果還沒獨立，可以把之前的 scan_repo 函式直接貼在這邊
try:
    from ast_scanner import scan_repo
except ImportError:
    # 若無獨立檔案，此處提供簡易 dummy 以防中斷
    def scan_repo(path): return {"utils/notifier.py": {"classes": [], "functions": [{"name": "send_legacy_sms", "args": ["phone_number", "message"], "returns": "bool"}]}}

# 初始化 LLM Client (請確保環境變數中有 OPENAI_API_KEY)
client = OpenAI()

# ==========================================
# 核心 Prompt 庫定義
# ==========================================
GATEKEEPER_PROMPT = """# Role
你是一個嚴格的程式碼規格審查員（Gatekeeper Agent）。你的職責是比對「輸入的 Spec」與「推論政策（Inference Policy）」，判斷 Spec 中模糊不清的地方是否觸犯了禁止推論的紅線。

# Output Format
你必須嚴格輸出以下 JSON 格式，不要包含任何額外的 Markdown 說明文字：
{
  "status": "APPROVED" 或 "REJECTED",
  "reason": "通過的理由，或者觸犯 Blocked 紅線的具體原因",
  "risks": ["具體風險或模糊點"]
}"""

ANALYSIS_PROMPT = """# Role
你是一位資深的 Python 軟體架構師。你需要對「規格需求（Spec）」與「既有程式庫特徵（Repo AST Summary）」進行深度分析，找出兩者的衝突點，並設計出相容兩者的 Adapter（適應器）架構。

# Core Strategy: 雙軌保留與模糊處理
1. **Adapter 模式 (方案乙)**：必須在同一個檔案內同時相容 Spec 與 Repo，使用 if/else 兼容，不允許拋棄任何一邊。
2. **模糊推論與 TODO**：在允許範圍內有模糊之處，請計劃在程式碼中插樁 `# TODO: AI 推論部分`。

# Output Format
請嚴格依據以下 JSON 格式輸出，不要包含額外的解釋文字：
{
  "conflicts": [{"description": "衝突點", "resolution_strategy": "解法"}],
  "inference_points": [{"location": "位置", "todo_comment": "# TODO: AI 推論部分 - 提示"}],
  "architecture_plan": {
    "class_name": "類別名稱",
    "required_imports": ["引用的模組"],
    "adapter_logic_summary": "架構概述"
  }
}"""

CODE_GEN_PROMPT = """# Role
你是一個精準的 Python 高級開發工程師。你的任務是嚴格根據「第一階段的分析計劃（Analysis JSON）」與「原始規格（Target Spec）」，編寫出高維護性、完全符合架構設計的 Python 程式碼。

# 實作鐵律
1. **Adapter 雙軌保留（方案乙）**：在同一個檔案內，使用 if/else 或資料映射，同時支援 Spec 規定的欄位與 Repo 既有的欄位。
2. **模糊推論與 TODO 插樁**：你必須在程式碼對應位置進行模糊推論，並且「必須」在該行程式碼上方精準加上註解 `# TODO: AI 推論部分 - [具體提示文字]`。
3. **零文字Filler**：只輸出可執行的 Python 程式碼，直接以 ```python 開始，不要有任何前後贅詞。"""

TEST_GEN_PROMPT = """# Role
你是一個精準的 QA 自動化工程師。你的任務是針對第二階段生成的「核心程式碼」撰寫高質量的 pytest 測試案例。

# 測試撰寫鐵律
1. **以 Spec 為基準線驗證**：實際測試案例（`test_*`）必須「只包含」符合 [Target Spec] 規範的輸入資料。
2. **相容分支透明化**：針對 Repo 相容性的測試程式碼以註解形式呈現。
3. **精準插樁註記**：在被註解的 Repo 測試上方，你「必須」加上 `# TODO: Repo branch untested` 註記。
4. **零文字 Filler**：只輸出可執行的 Python 程式碼，直接以 ```python 開始，不要有任何前後贅詞。"""

# ==========================================
# 工具函式
# ==========================================
def call_llm(system_prompt, user_content, is_json=False):
    """通用 LLM 呼叫封裝"""
    response_format = {"type": "json_object"} if is_json else {"type": "text"}
    completion = client.chat.completions.create(
        model="gpt-4o",  # 可替換為合適的平衡型大模型
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        response_format=response_format,
        temperature=0.2 # 程式碼生成需要低隨機性
    )
    return completion.choices[0].message.content

def extract_code_block(llm_output):
    """清洗 LLM 輸出的 Markdown Code Block 標籤"""
    lines = llm_output.strip().split('\n')
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines[-1].startswith("```"):
        lines = lines[:-1]
    return '\n'.join(lines)

# ==========================================
# CLI 主調度邏輯
# ==========================================
def main():
    parser = argparse.ArgumentParser(description="Agent Skill Generator CLI Orchestrator")
    parser.add_argument("--spec", required=True, help="Path to the target spec text file")
    parser.add_argument("--repo", default="./my_agent_repo", help="Path to the repository to scan")
    parser.add_argument("--policy", default="inference_policy.md", help="Path to the inference policy MD file")
    parser.add_argument("--output_dir", default="./generated_skills", help="Target output folder")
    args = parser.parse_args()

    # 讀取輸入檔案
    if not os.path.exists(args.spec) or not os.path.exists(args.policy):
        print(f"❌ 錯誤: 找不到 Spec 檔案 ({args.spec}) 或 政策檔案 ({args.policy})")
        sys.exit(1)

    with open(args.spec, "r", encoding="utf-8") as f:
        target_spec = f.read()
    with open(args.policy, "r", encoding="utf-8") as f:
        inference_policy = f.read()

    print("🔍 [Step 0] 正在即時動態掃描 Repo AST 特徵...")
    repo_ast_summary = scan_repo(args.repo)

    # ------------------------------------------
    # 🛡️ 步驟 1: Gatekeeper 審查
    # ------------------------------------------
    print("🛡️ [Step 1] 啟動 Gatekeeper 邊界審查中...")
    gatekeeper_input = f"[Inference Policy]:\n{inference_policy}\n\n[Input Spec]:\n{target_spec}"
    gatekeeper_res = json.loads(call_llm(GATEKEEPER_PROMPT, gatekeeper_input, is_json=True))

    if gatekeeper_res.get("status") == "REJECTED":
        print(f"❌ 安全阻斷：Spec 內容觸犯推論紅線！")
        print(f"原因: {gatekeeper_res.get('reason')}")
        sys.exit(1)
    print(f"✅ 審查通過。風險提示: {gatekeeper_res.get('risks')}")

    # ------------------------------------------
    # 📊 步驟 2: Conflict & Adapter 分析
    # ------------------------------------------
    print("📊 [Step 2] 啟動第一階段架構分析...")
    analysis_input = f"[Target Spec]:\n{target_spec}\n\n[Repo AST Summary]:\n{json.dumps(repo_ast_summary)}"
    analysis_res = call_llm(ANALYSIS_PROMPT, analysis_input, is_json=True)
    analysis_json = json.loads(analysis_res)
    
    # 取得預計生成的 Skill 檔案名稱
    class_name = analysis_json.get("architecture_plan", {}).get("class_name", "GeneratedSkill")
    file_base_name = "".join(["_" + c.lower() if c.isupper() else c for c in class_name]).lstrip("_")
    print(f"ℹ️ 預計產出技能名稱: {class_name}")

    # ------------------------------------------
    # 💻 步驟 3: 核心程式碼生成
    # ------------------------------------------
    print("💻 [Step 3] 正在生成雙軌相容核心程式碼 (方案乙)...")
    code_gen_input = f"[Target Spec]:\n{target_spec}\n\n[Analysis JSON]:\n{analysis_res}"
    raw_code = call_llm(CODE_GEN_PROMPT, code_gen_input)
    clean_code = extract_code_block(raw_code)

    # ------------------------------------------
    # 🧪 步驟 4: pytest 測試案例生成
    # ------------------------------------------
    print("🧪 [Step 4] 正在生成符合 Spec 基準之 pytest 測試案例...")
    test_gen_input = f"[Target Spec]:\n{target_spec}\n\n[Generated Code]:\n{clean_code}"
    raw_test = call_llm(TEST_GEN_PROMPT, test_gen_input)
    clean_test = extract_code_block(raw_test)

    # ------------------------------------------
    # 💾 步驟 5: 檔案寫入與落盤
    # ------------------------------------------
    print("💾 [Step 5] 正在將結果寫入目標資料夾...")
    skill_dir = os.path.join(args.output_dir, file_base_name)
    os.makedirs(skill_dir, exist_ok=True)

    code_path = os.path.join(skill_dir, f"{file_base_name}.py")
    test_path = os.path.join(skill_dir, f"test_{file_base_name}.py")

    with open(code_path, "w", encoding="utf-8") as f:
        f.write(clean_code)
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(clean_test)

    print(f"\n🎉 成功！一整套 Skill 資料夾已產出於: {skill_dir}")
    print(f"   └─ 核心程式碼 (含 # TODO: AI 推論部分): {code_path}")
    print(f"   └─ 測試案例 (含 # TODO: Repo branch untested): {test_path}")

if __name__ == "__main__":
    main()
