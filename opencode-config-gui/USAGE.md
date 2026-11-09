# opencode-config-gui — Usage

## Install / Build

```bash
# Prerequisites: Rust toolchain
curl -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
source $HOME/.cargo/env

# Build
cd /home/sam/代理人/opencode-config-gui
cargo build            # debug
cargo build --release  # release
```

Verification:
```bash
cargo --version   # cargo 1.99.1
rustc --version   # rustc 1.99.1
ls target/release/opencode-config-gui
```

## Run

GUI (requires display):
```bash
./target/release/opencode-config-gui
```

Headless:
```bash
./target/release/opencode-config-gui --dump               # stdout Markdown
./target/release/opencode-config-gui --export out.md      # write file
./target/release/opencode-config-gui --help
```

## Scenario Table

| Situation | Playbook | Primary tool |
|---|---|---|
| Browse opencode settings | Run GUI, OpenCode tab, search | `opencode-config-gui` |
| Browse grok settings | Run GUI, Grok tab | `opencode-config-gui` |
| Browse CrewAI agent fields | Run GUI, CrewAI tab | `opencode-config-gui` |
| Headless report / CI | `--dump` or `--export` | `opencode-config-gui` |
| Refresh opencode schema | Click "Fetch live schema" or re-download data/opencode_schema.json | GUI / curl |

## Path Quick-Reference

| Path | Purpose |
|---|---|
| `src/main.rs` | Application code |
| `Cargo.toml` | Dependencies |
| `data/opencode_schema.json` | OpenCode config schema |
| `data/opencode_agents.json` | Built-in agents |
| `data/grok_config.json` | Grok config keys |
| `data/grok_agents.json` | Grok bundled agents |
| `data/crewai_agent.json` | CrewAI Agent fields |
| `target/release/opencode-config-gui` | Release binary |
