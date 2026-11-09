# 雲端佈署服務性價比比較 (AWS / Cloudflare / Render / Railway)

## 總覽

| 項目 | AWS | Cloudflare | Render | Railway |
|------|-----|------------|--------|---------|
| 免費層 | 12 個月 (EC2 t2.micro) | Workers 免費 (100k req/day) | Free (休眠) | $5/月 credit |
| 容器支援 | ECS/Fargate (付費) | Containers (Workers) | Web Service (Docker) | Docker (原生) |
| Streamlit 適配 | ✅ EC2/ECS | ✅ Containers | ✅ Docker | ✅ Docker |
| 冷啟動 | 無 (EC2) / 有 (Lambda) | 有 (Workers) | 有 (Free plan 休眠) | 低 |
| 全球 CDN | ✅ (CloudFront) | ✅ (原生) | 有限 | 有限 |
| 學習曲線 | 高 | 中 | 低 | 低 |
| 設定複雜度 | 高 | 中 | 低 | 低 |

## 成本比較（月費估算，Streamlit 應用）

| 方案 | AWS | Cloudflare | Render | Railway |
|------|-----|------------|--------|---------|
| 免費/試用 | 12 個月 EC2 t2.micro | Workers 免費層 | Free (休眠 15min) | $5 credit/月 |
| 小型 (1 instance) | ~$10-30 (t3.micro) | ~$5 (Workers Paid) | $7 (Starter) | ~$5-10 |
| 中型 (2 instances) | ~$30-60 | ~$5-10 | $14-25 | ~$10-20 |
| 大型 (auto-scale) | $100+ | ~$10-50 | $25+ | $20+ |

## 性能比較

| 指標 | AWS | Cloudflare | Render | Railway |
|------|-----|------------|--------|---------|
| 全球延遲 | 低 (多區域) | 極低 (Edge) | 中 (單區域) | 中 (單區域) |
| 冷啟動時間 | N/A (EC2) | ~50ms (Workers) | ~30s (Free 休眠) | ~5s |
| 可用性 SLA | 99.99% | 99.99% | 99.95% | 99.9% |
| 擴展性 | 極高 | 高 | 中 | 中 |

## 適用場景

| 場景 | 推薦 |
|------|------|
| 個人/原型 | Render Free 或 Railway |
| 小型正式 | Railway 或 Cloudflare Workers |
| 全球低延遲 | Cloudflare |
| 企業級/合規 | AWS |
| Docker 原生 | Railway / Render |
| 成本敏感 | Cloudflare Free → Render Free |

## 本專案建議
- **代理人 (Streamlit)**：Render Free（簡單）或 Railway（Docker 原生）。
- **量傳線 (Streamlit + LibreOffice)**：Railway（映像較大，Render Free 可能超時）。
- **技能/靜態資源**：Cloudflare Pages（免費、全球 CDN）。
- **大規模/企業**：AWS ECS + CloudFront。

## 結論
- **最佳性價比（小專案）**：Railway ($5/月) 或 Render Free。
- **最佳全球性能**：Cloudflare。
- **最佳企業級**：AWS（但成本與複雜度高）。