---
name: cloud-deploy
description: Use when the user wants to deploy or verify an application to a cloud/hosting platform, set up CI/CD, or troubleshoot deployment configuration, and asks to 佈署、deploy、雲端、CI/CD、Docker、health check、部署驗證.
---

# Deployment & Verification Capability（可移植）

本 skill 提供**部署、CI/CD 與驗證**的通用流程。規範用中性佔位（6B）；公開平台/工具名稱與通用操作結構可保留，機密（token/key/account）不得入規範或提交。

## 流程（範本）
1. **前置**：帳號/權限、目標環境（`<platform>`）、網域/網路限制、機密管理方式。
2. **設定**：容器/執行環境、依賴、啟動命令、環境變數（機密由秘密管理）、健康檢查端點。
3. **CI/CD（可選）**：建置→測試→部署；權限最小化；產出可追溯版本/commit/tag。
4. **部署**：依平台執行部署；保留部署記錄與版本識別。
5. **驗證**：health/readiness、關鍵頁/API、log/錯誤率、回滾條件；**未驗證不得宣稱部署成功**。

## 驗證證據（對齊 C1）
- 環境/版本、命令或 pipeline ref、觀測結果（HTTP/status/log 摘要）、pass/fail、timestamp、evidence ref。

## 安全
- 機密僅存於平台秘密/本機安全設定；文件與 skill 使用 `<token>/<secret>` 佔位。
- 權限不足、網域/路由/建置依賴缺失屬常見阻塞，需記錄並修正後重驗。

## Contract Reference (stable)
引用 `qcable-contracts`（C1）：Evidence、gate rule、stop-the-line、Change control。部署狀態不明或驗證失敗 → 不得宣稱成功。

## 交棒（capability）
- 產品/功能驗收 → `acceptance/KPI gate capability`；測試 → `test/SOP capability`；選路/重構 → `index/orchestration capability`。

## Reference implementation (non-normative example, 1b)
> 參考實作範例，非規範依賴。`<workspace>` 可包含 `Dockerfile`、平台設定檔、CI workflow、驗證腳本；具體 provider 設定、帳號、網域與路徑依 6B/專案。公開 CLI/平台文件可查閱對應官方來源。