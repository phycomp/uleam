# opencode-config-gui — Test Report

## Environment

| Item | Value |
|---|---|
| OS | Linux (WSL2) |
| Rust | rustc 1.99.1 (58cf8f9c3 2026-10-13) |
| Cargo | cargo 1.99.1 (5f94df478 2026-08-27) |
| Project | /home/sam/代理人/opencode-config-gui |
| Date | 2026-11-06 |

## Test Results

Suite: `opencode_config_gui.sh` (headless)

| # | Test | Result |
|---|---|---|
| 1 | cargo build (debug) | PASS |
| 2 | cargo build --release | PASS |
| 3 | --help exits 0 | PASS |
| 4 | --dump header present | PASS |
| 5 | --export produces non-empty file | PASS |
| 6 | content: "OpenCode — top-level settings" | PASS |
| 7 | content: "OpenCode — AgentConfig fields" | PASS |
| 8 | content: "Grok — config sections" | PASS |
| 9 | content: "CrewAI — Agent fields" | PASS |

Total: PASS=9, FAIL=0.

Captured run:
```
=== cargo build (debug) ===
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
[PASS]
...
PASS=9  FAIL=0
```

Manual verification:
- `--dump` outputs 699 lines of Markdown.
- `--export /tmp/opencode/gui_report.md` writes 699 lines.
- All four section headers present.

## Known Limitations

- GUI mode cannot run in this headless environment (MESA/ZINK no GPU); use `--dump`/`--export`.
- Live schema fetch requires network; offline falls back to bundled `data/opencode_schema.json`.
- Schema data is a snapshot; re-download periodically to stay current.
