# Target Spec: Notifier Skill

## Goal
提供一個可重用的通知技能，支援 SMS 與 Email 兩種通道，並能依優先順序 fallback。

## Interface
- class Notifier
  - __init__(self, channels: list[str])
  - send(self, message: str, recipient: str) -> bool
  - send_bulk(self, messages: list[str], recipients: list[str]) -> list[bool]

## Constraints
- 必須保留既有 Repo 中的 send_legacy_sms(phone_number, message) 函式相容。
- 不得在未經確認的情況下發送真實訊息（測試模式）。
- 所有模糊處以 # TODO: AI 推論部分 標註。

## Inputs
- channels: ["sms", "email"] 或子集
- message: str
- recipient: str (phone or email)