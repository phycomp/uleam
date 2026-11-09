# my_agent_repo/utils/notifier.py
def send_legacy_sms(phone_number: str, message: str) -> bool:
    """
    發送簡訊通知。
    注意：Repo 舊系統規定，內部的欄位名稱必須是 phone_number。
    """
    print(f"SMS sent to {phone_number}: {message}")
    return True
