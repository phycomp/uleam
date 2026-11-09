# 量子傳輸線驗收 Pipeline 使用說明

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

## KPI 驗收結果
- 整體通過：YES
- 階段數：5
  - Stage 0 KPI 規格指標: pass
  - Stage 1 開發量子傳輸線: pass
  - Stage 2 測試: pass
  - Stage 3 驗證: pass
  - Stage 4 交付: pass

## 材料數據庫
資料位於 `acceptance_pipeline/materials.json`，API：`MaterialDB`。

## 交付物
- 程式碼：acceptance_pipeline/
- 測試：tests/test_acceptance_pipeline.py
- 驗收標準：acceptance_pipeline/acceptance_criteria.yaml
- 報告：acceptance_output/acceptance_report.json
