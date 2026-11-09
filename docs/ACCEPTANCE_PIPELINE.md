# 驗收 Pipeline 使用說明

## 安裝
```bash
cd /home/sam/代理人
pip install -r requirements.txt
```

## 執行
```bash
python -c "from acceptance_pipeline.pipeline import AcceptancePipeline; print(AcceptancePipeline().run().overall_pass)"
```

## 測試
```bash
pytest tests/test_acceptance_pipeline.py -v
```

## 階段
0. KPI 規格指標
1. 開發量子傳輸線
2. 測試
3. 驗證
4. 交付
5. 使用說明+測試+材料數據庫
6. 各階段 KPI 驗收

## 材料數據庫
- 檔案：`acceptance_pipeline/materials.json`
- API：`MaterialDB` (`get`, `list_all`, `search`, `add`)

## 驗收標準
- 檔案：`acceptance_pipeline/acceptance_criteria.yaml`
- 驗證器：`AcceptanceValidator.validate(results)`

## 交付物
- 程式碼：`acceptance_pipeline/`
- 測試：`tests/test_acceptance_pipeline.py`
- Streamlit：`pages/11驗收Pipeline.py`
- CI：`scripts/run_acceptance.sh`
- 報告：`acceptance_output/`

## KPI
KPI-1..KPI-5 全部追蹤，詳見 `acceptance_pipeline/kpi_spec.yaml`。