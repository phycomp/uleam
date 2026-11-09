【技能名稱】: SendAlertSkill
【輸入參數】: 
  - cellphone (string): 接收通知的手機號碼
  - text (string): 通知內容
  - priority (string, optional): 通知層級。若未提供，請 AI 自行推論合理的預設值。
【核心邏輯】: 
  接收參數後，必須呼叫專案內既有的 notifier 工具發送通知。
