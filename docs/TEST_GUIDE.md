# 測試指南 (Test Guide)

## 測試範圍

### 1. Smoke Tests（全技能）
```bash
cd /home/sam/代理人
python examples/test_example.py
```
彙總所有技能的 smoke tests，應全部 PASS。

### 2. 單一技能測試
```bash
cd /home/sam/代理人
python generated_skills/<skill>/test_<skill>.py
```
例如：
```bash
python generated_skills/impedance_calculator/test_impedance_calculator.py
python generated_skills/thermal_load/test_thermal_load.py
python generated_skills/cross_section_renderer/test_cross_section_renderer.py
python generated_skills/agent_workflow/test_agent_workflow.py
python generated_skills/dsl_parser/test_dsl_parser.py
python generated_skills/notifier/test_notifier.py
python generated_skills/greeter/test_greeter.py
```

### 3. 編譯檢查
```bash
cd /home/sam/代理人
python -m py_compile 計算.py 代理主程式.py 疊構Util.py 元件整合.py app.py ast_scanner.py
```

### 4. 執行範例
```bash
cd /home/sam/代理人
python examples/run_example.py
```

## 測試文件位置
- `examples/test_example.py`：彙總 smoke tests
- `generated_skills/<skill>/test_<skill>.py`：單一技能測試
- 各技能測試使用 `importlib.util` 載入，避免模組名稱衝突

## 測試撰寫規範
- 以 Spec 為基準線驗證。
- Repo 相容分支以註解呈現，加上 `# TODO: Repo branch untested`。
- 模糊推論處插樁 `# TODO: AI 推論部分`。

## 常見問題
- **pytest 未安裝**：使用 `python <test_file>.py` 直接執行（測試檔含 `if __name__` 或頂層 assert）。
- **模組名稱衝突**（如 `notifier`）：使用 `importlib.util.spec_from_file_location` 載入。