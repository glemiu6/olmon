# 🛣️ olmon — Roadmap

---

## v0.1.0 — Foundation 
> Goal: Working CLI, can talk to Ollama

- [x] Project setup (`rich` + `argparse` + `httpx`)
- [x] `client.py` — Ollama API wrapper
- [x] `status` command
- [x] `models` command with sort and filter
- [x] `inspect` command
- [x] `ps` command
- [x] `watch` live dashboard
- [x] `init` command
- [x] `update` command
- [x] `uninstall` command
- [x] Config file (`~/.config/olmon/config.json`)
- [x] `--host` flag override
- [x] PyPI publish
- [x] GitHub Actions CI/CD
- [x] Linux x86_64 and macOS arm64 binaries

---

## v0.2.0 — Scripting & Power Users 
> Goal: Make olmon the DevOps-friendly Ollama tool

- [x] `olmon stop <model>` — force unload a model from VRAM
- [x] `olmon compare <model1> <model2> ...` — side by side spec comparison
- [x] `olmon top` — htop-style live view with VRAM usage and expiry countdown
- [x] `--json` flag on every command
- [x] `--no-color` flag for pipe-friendly output
- [x] Proper exit codes (0 / 1 / 2) on every command
- [x] VRAM used / total shown in `olmon status` (NVIDIA)
- [x] Fixed macOS SSL issue by switching to `httpx`

---

## v0.3.0 — Hardware Awareness
> Goal: Know your hardware limits before they hit you

- [ ] `olmon fit <model>` — will this model fit in my VRAM?
  - installed models → read from `get_model_info()`
  - uninstalled models → lookup from SQLite db
- [ ] `olmon recommend --vram 8GB` — suggest models that fit
- [x] `olmon db update` — scrape ollama.com and populate local SQLite
- [x] `olmon db stats` — how many models cached
- [ ] `olmon search <query>` — search local SQLite db
- [ ] Warn in `watch` and `top` when VRAM usage above 90%
- [ ] GPU temperature and power draw (NVIDIA via `nvidia-smi`)
- [ ] AMD GPU support

---

## v0.4.0 — Discovery & Library
> Goal: Explore models without leaving the terminal

- [ ] `olmon biggest` — show largest installed models
- [ ] `olmon smallest` — show smallest installed models
- [ ] `olmon unused` — models not used in the last N days
- [ ] Model capabilities filter in `models` (`--capability vision`)
- [ ] `olmon info <model>` — show library info for uninstalled models
- [ ] Pagination support for `olmon search`

---

## v0.5.0 — Interactive TUI
> Goal: Transform olmon into a full-screen terminal dashboard

- [ ] Switch to Textual framework
- [ ] Keyboard navigation
- [ ] Mouse support
- [ ] Help screen (`?`)
- [ ] Search (`/`)
- [ ] Sorting (`s`) and filtering (`f`)
- [ ] Models view — interactive table
  - Inspect selected model
  - Unload model (`u`)
  - Live expiry countdown
- [ ] Dashboard view
  - Live VRAM graph
  - GPU usage graph
  - CPU and RAM monitoring
- [ ] Multi-screen interface (Models / GPU / Settings)
- [ ] Footer with keyboard shortcuts

---

## v0.6.0 — History & Analytics
> Goal: Understand how you use your models

- [ ] SQLite usage database (`~/.config/olmon/history.db`)
- [ ] Track which models were loaded and when
- [ ] `olmon history` — show usage history
- [ ] `olmon history --model qwen2.5:7b` — filter by model
- [ ] `olmon stats` — total runtime, most used, last used per model
- [ ] Daily and weekly usage summaries

---

## v0.7.0 — Benchmarks
> Goal: Measure and compare model performance

- [ ] `olmon bench <model>` — run benchmark prompt, measure TPS and VRAM
- [ ] `olmon bench <model1> <model2>` — compare performance side by side
- [ ] Benchmark history stored in SQLite
- [ ] Peak VRAM and RAM per benchmark
- [ ] Community benchmark upload (opt-in anonymous results)
- [ ] `olmon fit` powered by community VRAM data

---

## v0.8.0 — Alerts & Automation
> Goal: React automatically to model events

- [ ] `olmon alert` — desktop notification when model loads/unloads
- [ ] `olmon watch --alert` — notify on state change
- [ ] Webhook support — POST to URL on model state change
- [ ] `olmon wait <model>` — block until model is loaded (for scripts)
- [ ] Event hooks for shell scripts

---

## v1.0.0 — Stable Release
> Goal: Production-ready, polished, and documented

- [ ] Full test coverage
- [ ] Windows support (WSL-free)
- [ ] Man page (`man olmon`)
- [ ] Shell autocomplete (bash + zsh + fish)
- [ ] Detailed docs site
- [ ] Performance audit — startup time under 100ms
- [ ] Plugin API
- [ ] Themes and accessibility improvements

---

## v1.1.0 — Plugin System
> Goal: Let the community extend olmon

- [ ] Plugin architecture
- [ ] `olmon plugins` — list installed plugins
- [ ] Official plugins:
  - `gpu-exporter` — Prometheus metrics
  - `discord-alerts` — Discord notifications
  - `grafana` — Grafana dashboard export
  - `slack` — Slack alerts
  - `prometheus` — metrics endpoint

---

## v2.0.0 — Browser Dashboard
> Goal: Web interface powered by the same backend

- [ ] `olmon serve` — start local web dashboard
- [ ] Real-time model monitoring in browser
- [ ] Usage history charts
- [ ] Multi-host support (monitor multiple Ollama servers)
- [ ] Remote management
- [ ] Authentication
- [ ] Dark / light mode