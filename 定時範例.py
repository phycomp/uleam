if __name__ == "__main__":
    # 預設的公司資料庫設定 (請依實際狀況修改)
    DATABASE_CONFIG = {
        "host": "127.0.0.1",
        "port": 5432,
        "user": "postgres",
        "password": "your_secure_password",
        "dbname": "quantum_db"
    }

    # 預設的物理約束 Spec (當命令列沒有傳入任何參數時作為備援)
    input_args = {
        "target_zo": 50.0,
        "thermal_budget_uw": 1.0,
        "min_h_mil": 4.0,
        "er_dielectric": 4.2
    }

    # 📥 核心邏輯：從命令列 (CLI) 讀取傳入的 Spec JSON
    # sys.argv[0] 是腳本名稱本身 (agent_production.py)
    # sys.argv[1] 才是第一個帶入的參數字串
    if len(sys.argv) > 1:
        try:
            raw_json_str = sys.argv[1]
            # 將傳入的 JSON 字串解析為 Python 字典 (Dictionary)
            input_args = json.loads(raw_json_str)
            print("📥 成功偵測到命令列自訂 Spec 參數。")
        except json.JSONDecodeError as e:
            print(f"⚠️ 參數 JSON 解析失敗 ({e})，自動採用系統預設 Spec 執行。")
    else:
        print("ℹ️ 未偵測到命令列參數，採用預設 Spec 執行。")

    # 打印本次執行的 Spec 內容，便於在 Linux Log 中查看
    print(f"📋 當前執行 Spec 參數: {json.dumps(input_args)}")

    # 執行優化
    print("🤖 Agent 啟動：開始進行多場梯度協同優化...")
    best_three_df = run_agent_optimization(input_args)

    # 寫入資料庫
    if not best_three_df.empty:
        save_to_postgresql(best_three_df, DATABASE_CONFIG)
    else:
        print("❌ 本次排程迭代未能收斂出滿足約束的解，未寫入資料庫。")
