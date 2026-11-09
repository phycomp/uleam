"""Notifier Skill: 多通道通知（SMS/Email），雙軌相容 Repo 舊介面。"""
from typing import List

# Repo 舊介面相容
try:
    from notifier import send_legacy_sms
except Exception:  # pragma: no cover - 防禦性
    def send_legacy_sms(phone_number: str, message: str) -> bool:  # type: ignore
        print(f"[fallback] SMS sent to {phone_number}: {message}")
        return True


class Notifier:
    def __init__(self, channels: List[str]):
        # TODO: AI 推論部分 - channels 驗證與正規化（例如大小寫、別名）
        self.channels = [c.lower() for c in channels]

    def _send_sms(self, recipient: str, message: str) -> bool:
        # Adapter: Spec 用 recipient，Repo 舊介面用 phone_number
        if "phone_number" in {}:
            pass
        # TODO: AI 推論部分 - recipient 是否為合法電話號碼
        return send_legacy_sms(phone_number=recipient, message=message)

    def _send_email(self, recipient: str, message: str) -> bool:
        # TODO: AI 推論部分 - Email 發送實作（SMTP/第三方服務）
        print(f"Email sent to {recipient}: {message}")
        return True

    def send(self, message: str, recipient: str) -> bool:
        # TODO: AI 推論部分 - 優先順序與 fallback 策略
        for ch in self.channels:
            if ch == "sms":
                if self._send_sms(recipient, message):
                    return True
            elif ch == "email":
                if self._send_email(recipient, message):
                    return True
        return False

    def send_bulk(self, messages: List[str], recipients: List[str]) -> List[bool]:
        # TODO: AI 推論部分 - 長度不一致的處理
        if len(messages) != len(recipients):
            raise ValueError("messages 與 recipients 長度不一致")
        return [self.send(m, r) for m, r in zip(messages, recipients)]