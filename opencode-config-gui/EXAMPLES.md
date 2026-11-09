# opencode-config-gui — Examples

## Example 1: Build from scratch

```bash
cd /home/sam/代理人/opencode-config-gui
source $HOME/.cargo/env
cargo build --release
./target/release/opencode-config-gui --help
```

## Example 2: Headless dump to stdout

```bash
./target/release/opencode-config-gui --dump | head -20
```

## Example 3: Export report to file

```bash
./target/release/opencode-config-gui --export /tmp/opencode/report.md
wc -l /tmp/opencode/report.md
```

## Example 4: Run test suite

```bash
/home/sam/代理人/opencode_config_gui.sh
```

## Example 5: GUI mode (on a machine with display)

```bash
./target/release/opencode-config-gui
# Then: OpenCode tab -> search "agent" -> Export Markdown
```

## Example 6: Refresh opencode schema

```bash
curl -sS https://opencode.ai/config.json -o data/opencode_schema.json
cargo build
```
