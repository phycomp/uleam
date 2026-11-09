import json
# 引入先前寫好的 AST 掃描器
from ast_scanner import scan_repo 

# ==========================================
# 0. 初始化資料與即時 AST 掃描
# ==========================================
print("🔍 步驟 0: 正在即時掃描 Repo 提取特徵...")
repo_ast_summary = scan_repo("./my_agent_repo")

# 讀取外部政策檔案
with open("inference_policy.md", "r", encoding="utf-8") as f:
    inference_policy_content = f.read()

# 模擬開發者輸入的 Spec
target_spec = """
【技能名稱】: SendAlertSkill
【輸入參數】: 
  - cellphone (string): 接收通知的手機號碼
  - text (string): 通知內容
  - priority (string, optional): 通知層級。若未提供，請 AI 自行推論合理的預設值。
【核心邏輯】: 
  接收參數後，必須呼叫專案內既有的 notifier 工具發送通知。
"""

# ==========================================
# 1. 前置檢查 Gatekeeper 階段
# ==========================================
print("\n🛡️ 步驟 1: Gatekeeper 正在進行邊界審查...")

# 這裡模擬 Gatekeeper Agent 的呼叫與 LLM 回傳的 JSON 
# (實作時請將下面的 Prompt 與 inputs 餵給你的 LLM API)
gatekeeper_mock_response = {
    "status": "APPROVED",
    "reason": "Spec 中要求的 priority 模糊屬於 Allowed 範疇（預設層級），且未涉及 Blocked 紅線（如修改 DB 或金鑰）。",
    "risks": ["priority 欄位需要 AI 進行模糊推論與插樁"]
}

if gatekeeper_mock_response["status"] == "REJECTED":
    raise Exception(f"❌ 安全中斷！觸犯推論紅線。原因: {gatekeeper_mock_response['reason']}")
else:
    print(f"✅ 審查通過！風險評估: {gatekeeper_mock_response['risks']}")

# ==========================================
# 2. 第一階段：Conflict & Adapter 分析階段
# ==========================================
print("\n📊 步驟 2: 啟動第一階段分析 (Conflict & Adapter 偵測)...")

# 這裡模擬主 Agent 接收到先前提供的「第一階段 Prompt」後的輸出結果
# (實作時，請將 Repo AST Summary 與 Target Spec 作為變數填入 Prompt 丟給 LLM)
analysis_mock_response = {
  "conflicts": [
    {
      "description": "Spec 要求的輸入欄位為 'cellphone'，但 Repo 現有的 send_legacy_sms 函數接收的參數名稱為 'phone_number'。",
      "resolution_strategy": "在同檔案內使用 Adapter 模式，初始化時建立對應關係，同時保留兩者，確保 inputs['cellphone'] 能正確映射至 phone_number。"
    }
  ],
  "inference_points": [
    {
      "location": "priority 參數解析邏輯",
      "todo_comment": "# TODO: AI 推論部分 - 當 priority 未提供時，自動盲猜並預設為 'INFO' 層級"
    }
  ],
  "architecture_plan": {
    "class_name": "SendAlertSkillAdapter",
    "required_imports": ["my_agent_repo.utils.notifier.send_legacy_sms"],
    "adapter_logic_summary": "建立 SendAlertSkillAdapter 類別。__init__ 接收 dict，同時支援 cellphone 與 phone_number 鍵值。execute 方法負責在推論預設 priority 後，呼叫 send_legacy_sms。"
  }
}

print("💡 [LLM 分析完成] 產出的結構化計劃書：")
print(json.dumps(analysis_mock_response, indent=2, ensure_ascii=False))

# ==========================================
# 後續預告：這個 analysis_mock_response JSON 
# 將會直接當作輸入，餵給第二階段的「程式碼生成 Prompt」
# ==========================================
