# 🛣️ Ollama Monitor CLI — Roadmap

---

## v0.1.0 — Foundation
> Goal: Working CLI skeleton can talk to Ollama

- [x] Project setup (`typer` + `rich` + `requests`)
- [x] `client.py` — basic Ollama API wrapper
- [x] `status` command
- [x] `models` command (simple table)
- [x] Config file (`~/.ollama-mon/config.json`)
- [x] `--host` flag override

---

## v0.2.0 — Core Monitoring
> Goal: The commands you'd use daily

- [ ] `ps` command with resource usage
- [ ] `models inspect <name>`
- [ ] `--json` flag on all commands
- [ ] `--no-color` flag
- [ ] Proper exit codes (0 / 1 / 2)

---

## v0.3.0 — Live Dashboard
> Goal: The "wow" feature

- [ ] `watch` command with auto-refresh
- [ ] Live status bar (🟢🔵🔴)
- [ ] Running models table updates in place
- [ ] `--interval` flag

---

## v0.4.0 — Polish & DX
> Goal: Feel like a real tool

- [ ] `config` command (set/show/reset)
- [ ] `--sort` and `--filter` on `models`
- [ ] Better error messages (offline, wrong URL, etc.)
- [ ] `--version` flag
- [ ] README + usage docs

---

## v0.5.0 — Distribution
> Goal: Others can install and use it

- [ ] Package for `pip install ollama-mon`
- [ ] PyPI publish
- [ ] GitHub Actions CI
- [ ] Releases with binaries (via PyInstaller)

---

## v1.0.0 — Stable
> Goal: Confident public release

- [ ] Full test coverage
- [ ] Docs site (or detailed README)
- [ ] Changelog
- [ ] MIT License file

---

## v2.0.0 — Power Features *(stretch)*
> Goal: The DevOps-friendly version

- [ ] `logs` command
- [ ] `alert` — notify on model state change
- [ ] `history` — SQLite usage tracking
- [ ] Remote profiles
- [ ] Browser dashboard (the migration you mentioned)