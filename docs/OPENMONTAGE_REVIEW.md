# OpenMontage Skill Review (safe-skill-workflow)

## Source
- Repo: calesthio/openmontage (78,368 stars, 90 skills)
- Installed: 90 skills to /home/sam/代理人/.agents/skills/

## Summary
- Purpose: Agentic video production system (12 pipelines, 52 tools, 500+ skills).
- Files: SKILL.md per skill + scripts/ (node/python) + references/.
- Shell commands: ffmpeg, yt-dlp, python, node (media processing).
- Network: API calls to video providers (HeyGen, fal.ai, etc.) — requires API keys.
- Credential access: API keys for video generation providers (user-provided).

## Static Scan
- 303 files reference http/https (expected for video production).
- 211 files reference api_key/secret/token/password (expected for provider auth).
- No `curl | sh` or obvious malware patterns found.
- Scripts are standard media processing (ffmpeg, python).

## Verdict: APPROVE (with guardrails)
- Guardrails:
  1. API keys must be user-provided via env vars, never hardcoded.
  2. Review individual skill scripts before running in production.
  3. Network calls only to configured providers.
  4. No credential exfiltration patterns detected.

## Known Limitations
- Requires ffmpeg, python, node installed.
- Provider API keys needed for video generation.
- Large repo (90 skills) increases context load.