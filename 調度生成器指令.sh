# 確保環境變數中有 API 金鑰
export OPENAI_API_KEY="your-api-key-here"

# 執行自動調度生成器
python orchestrator.py \
  --spec ./my_specs/new_skill_spec.txt \
  --repo ./my_agent_repo \
  --policy ./inference_policy.md \
  --output_dir ./generated_skills
