---
name: pqc-crypto
description: "後量子密碼 (PQC) 技能：ML-KEM-768、ML-DSA-65、Signal Protocol 後量子強化、X3DH-PQC、Double Ratchet。Use when the user wants to learn/implement post-quantum cryptography, ML-KEM, ML-DSA, Signal Protocol PQC, or quantum key distribution."
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---
# PQC Crypto — 後量子密碼

## 專案來源
- `/home/sam/PQC`：Signal PQC 通訊系統（ML-KEM-768 + ML-DSA-65 + Signal Protocol）。
- `/home/sam/橢圓加密`：ECC/PQC/QKD 教學與模擬。

## 核心演算法
- **ML-KEM-768** (FIPS 203)：金鑰封裝，PK 1184B, SK 2400B, CT 1088B。
- **ML-DSA-65** (FIPS 204)：數位簽章，SIG 3293B。
- **Hybrid KEM**：ML-KEM-768 + X25519（雙重保障）。
- **X3DH-PQC**：Signal X3DH 後量子強化（4-way DH + KEM）。
- **Double Ratchet**：對稱 + DH + KEM 棘輪。
- **群組通訊**：二叉樹群組金鑰管理。

## 教學內容（橢圓加密）
- ECC 加解密、橢圓曲線數學原理。
- PQC 專欄、QKD 密鑰分發。
- 量子密碼光偏振、量子圖像加密。

## 觸發條件
- 「PQC」「後量子密碼」「ML-KEM」「ML-DSA」「Signal Protocol」「QKD」「橢圓加密」「ECC」