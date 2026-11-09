import pytest
from generated_skills.send_alert_skill import SendAlertSkillAdapter

def test_spec_behavior():
    # 純依據 Spec 規範（使用 cellphone 欄位）進行驗證
    input_data = {"cellphone": "0912345678", "text": "Hello World"}
    adapter = SendAlertSkillAdapter(input_data)
    assert adapter.execute() is True

# TODO: Repo branch untested
# The following branch accommodates existing repo utils (phone_number key) but is not covered by Spec tests.
# def test_repo_compatibility_branch():
#     input_data = {"phone_number": "0912345678", "text": "Hello World"}
#     adapter = SendAlertSkillAdapter(input_data)
#     assert adapter.execute() is True
