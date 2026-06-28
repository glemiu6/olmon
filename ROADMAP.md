# olmon Roadmap


---

## v0.0.0 — Foundation ✅
> **Goal:** Working CLI, can talk to Ollama

- ✅ Project setup (rich + argparse + urllib)
- ✅ `client.py` — Ollama API wrapper
- ✅ `status` command
- ✅ `models` command with sort and filter
- ✅ `inspect` command
- ✅ `ps` command
- ✅ `watch` live dashboard
- ✅ `init` command
- ✅ `update` command
- ✅ `uninstall` command
- ✅ Config file (`~/.config/olmon/config.json`)
- ✅ `--host` flag override
- ✅ PyPI publish
- ✅ GitHub Actions CI/CD
- ✅ Linux + macOS binaries

---

## v0.1.0 — Scripting & Power Users
> **Goal:** Make olmon the DevOps-friendly Ollama tool

- ✅ `--json` flag on every command
- ✅ Proper exit codes (0 / 1 / 2) on every command
- ✅ `olmon stop <model>` — force unload a model from VRAM
- ✅ `olmon compare <model1> <model2>` — side by side spec comparison
- [ ] `--no-color` flag for pipe-friendly output
- [ ] `olmon top` — htop-style live view of all running models (CPU%, VRAM, tokens/min)
- [ ]  Request history & replay — log every prompt/response with token counts

---

## v0.2.0 — Hardware Awareness
> **Goal:** Know your hardware limits before they hit you

- [ ] Show total VRAM vs used VRAM in `status`
- [ ] Warn in `watch` when VRAM usage is above 90%
- [ ] GPU info panel in `status` (NVIDIA + AMD)
- [ ]  Electricity cost estimation per query for local models
- [ ]  "This model is using 80% of your VRAM" smart warnings
- [ ]  Recommend smaller quantization if resources are tight

---

## v0.3.0 — Discovery
> **Goal:** Explore models without leaving the terminal

- [ ] `olmon search <query>` — search Ollama library from terminal (scrapes ollama.com/search)
- [ ]  `olmon search <query> --source all` — search Ollama + HuggingFace + OpenAI in one command
- [ ]  Search results show size, quantization, benchmark scores inline
- [ ] `olmon biggest` — show largest installed models
- [ ] `olmon smallest` — show smallest installed models
- [ ] `olmon unused` — models not used in the last N days
- [ ] Model tags and capabilities filter in `models`
- [ ] `olmon fit <model>` — will this model fit in my VRAM?
- [ ] `olmon recommend --vram 6GB` — suggest models that fit your hardware

---

## v0.4.0 — History & Usage Tracking
> **Goal:** Know how you use your models over time

- [ ] SQLite local database (`~/.config/olmon/history.db`)
- [ ] Track which models were loaded and when
- [ ] `olmon history` — show usage history
- [ ] `olmon history --model qwen2.5:7b` — filter by model
- [ ] `olmon stats` — total runtime per model, most used, last used
- [ ]  `olmon history --replay <id>` — replay a past prompt across models
- [ ]  Per-model latency stats (p50, p95 response times)

---

## v0.5.0 — Alerts & Automation
> **Goal:** React to model state changes automatically

- [ ] `olmon alert` — desktop notification when model loads/unloads
- [ ] `olmon watch --alert` — notify on state change during watch
- [ ] Webhook support — POST to a URL on model state change
- [ ] `olmon wait <model>` — block until a model is loaded (for scripts)
- [ ]  `olmon bench <model1> <model2>` — run same prompt on both, compare speed & output
- [ ]  Token usage shown per response with `--verbose` flag

---

## v0.6.0 — Cloud & Unified Monitoring 🆕
> **Goal:** Monitor local + cloud models in one place

- [ ]  Connect OpenAI, Anthropic, and OpenAI-compatible APIs via config
- [ ]  `olmon ps` shows cloud models alongside local ones
- [ ]  `olmon cost` — monthly spend across local + cloud
- [ ]  Unified token tracking across all providers
- [ ]  `olmon compare <local-model> <cloud-model>` — cross-provider comparison

---

## v1.0.0 — Stable & Polished
> **Goal:** Confident public release

- [ ] Full test coverage
- [ ] Windows support (WSL-free)
- [ ] Man page (`man olmon`)
- [ ] Shell autocomplete (bash + zsh + fish)
- [ ] Detailed docs site
- [ ] Changelog
- [ ] Performance audit — startup time under 100ms

---

## v2.0.0 — Browser Dashboard
> **Goal:** The GUI version, built on top of the CLI

- [ ] `olmon serve` — start a local web dashboard
- [ ] Real-time model monitoring in the browser
- [ ] Usage history charts
- [ ] Multi-host support (monitor multiple Ollama servers)
- [ ]  Cross-provider cost dashboard (local + cloud side by side)
- [ ]  Model benchmarking visualizations
- [ ] Dark / light mode