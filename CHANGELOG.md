# Changelog

All notable changes to this project will be documented in this file.

---
## [0.2.0]

### Added
- `olmon top` - htop-style monitoring for running models
- VRAM used / total shown in `olmon status` (NVIDIA GPUs)
- `--no-color` flag for pipe-friendly output

## [0.1.3] - 2026-06-28

### Added
- `olmon compare` — side by side comparison of multiple models
- `--json` flag on all commands for scriptable output

### Fixed
- Fixed duplicate update notification when running `olmon update`

---

## [0.1.2] - 2026-06-27

### Added
- `olmon stop <model>` — unload a model from VRAM
- Proper exit codes on all commands (0 success, 1 offline, 2 error)

### Fixed
- Fixed permission denied error when installing from `/usr/local/bin`
- Fixed binary name typo (`komit` → `olmon`) in `install.sh`
- Fixed `get_latest_version()` returning empty string causing `v` version tag
- Added `--fail` flag to curl in `install.sh` to prevent saving HTML error pages as binaries
- Fixed `bool(input(...))` always returning `True` in `init` command
- Fixed `keep_alive: 0` not being passed correctly in `stop` command

---


## [0.1.0] - 2026-06-23

### Added
- `olmon status` — check Ollama connection, version, and model counts
- `olmon models` — list all installed models with size, family, quantization
- `olmon models --sort` — sort by name, size, or date
- `olmon models --filter` — filter models by name or family
- `olmon inspect <model>` — full details on a specific model
- `olmon ps` — show currently running models with VRAM usage
- `olmon watch` — live auto-refreshing dashboard
- `olmon watch --interval` — configurable refresh rate
- `olmon init` — interactive config file setup
- `olmon update` — update to latest version
- `olmon uninstall` — remove olmon and config
- `--host` global flag to override API URL per command
- `--version` flag
- Color-coded status indicators (🟢 🔵 🔴)
- Config file at `~/.config/olmon/config.json`
- Linux x86_64 and macOS arm64 binaries
- PyPI package (`pip install olmon`)
- GitHub Actions CI/CD for automated releases
- Install script (`curl | sh`)
- Automatic update check on every command

---

[0.2.0]: https://github.com/glemiu6/olmon/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/glemiu6/olmon/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/glemiu6/olmon/compare/v0.1.0...v0.1.2
[0.1.0]: https://github.com/glemiu6/olmon/releases/tag/v0.1.0