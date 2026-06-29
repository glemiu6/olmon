# olmon

A lightweight CLI to monitor your Ollama models and usage in real time.

---

[![PyPI](https://img.shields.io/pypi/v/olmon)](https://pypi.org/project/olmon)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/olmon?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/olmon)
[![License](https://img.shields.io/github/license/glemiu6/olmon)](https://github.com/glemiu6/olmon/blob/master/LICENSE)

```
$ olmon top

╭─────────────────────────────────────── olmon top 01:09:32 ───────────────────────────────────────╮
│ Model                        VRAM              VRAM %            Expires In      Status          │
│ ornith:9b                    5.0 GB            ██░░░  41%        0m 22s          ● expiring      │
│ phi4-mini:latest             2.9 GB            █░░░░  23%        0m 17s          ● expiring      │
╰────────────────────────────── VRAM: 7.8 GB / 12.0 GB |  2 running ───────────────────────────────╯



```

---

## Features

- 🔄 **Real-time dashboard** — live auto-refreshing view of running models
- 📋 **Model listing** — browse all installed models with size, family, and quantization
- 🔍 **Model inspection** — full details on any installed model
- 🟢 **Status indicators** — green / blue / red at a glance
- ⚙️ **Configurable** — set your API host and refresh interval
- 🪶 **Lightweight** — minimal dependencies, works over SSH on headless servers
- 🖥️ **htop-style monitoring** — `olmon top` with VRAM usage and expiry countdown
- 🛑 **Model control** — force unload models from VRAM
- ⚖️ **Model comparison** — side by side spec comparison of multiple models
- 🔧 **Scripting friendly** — `--json` flag and exit codes on every command

---

## Requirements

- Python 3.13+
- [Ollama](https://ollama.com) installed and running

---

## Installation

### pip

```bash
pip install olmon
```

### curl (Linux / macOS)

```bash
curl -fsSL https://raw.githubusercontent.com/glemiu6/olmon/master/scripts/install.sh | sh
```

### From source

```bash
git clone https://github.com/glemiu6/olmon.git
cd olmon
uv pip install -e .
```
### Windows

Native Windows binary is not currently supported.  
Use [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) and follow the Linux installation instructions.

---

## Usage

```bash
olmon status               # quick health check
olmon models               # list all installed models
olmon models --sort size   # sort by size
olmon models --filter llama  # filter by name or family
olmon inspect llama3:latest  # full details on a model
olmon ps                   # show currently running models
olmon watch                # live auto-refreshing dashboard
olmon watch --interval 5   # refresh every 5 seconds
olmon top                  # htop-style live monitoring
olmon stop qwen2.5:7b      # unload a model from VRAM
olmon compare qwen2.5:7b llama3.2:latest  # compare models
olmon --no-color models    # pipe-friendly output
olmon models --json        # output as JSON
```

### Global flags

```bash
olmon --host http://192.168.1.10:11434 status   # connect to remote Ollama
olmon --version                                  # print version
```

---

## Status Indicators

| Indicator | Meaning |
|-----------|---------|
| 🟢 Green  | Models are loaded and running |
| 🔵 Blue   | Ollama is idle, no models loaded |
| 🔴 Red    | Ollama is offline or unreachable |

---

## Configuration

```bash
olmon init          # create default config file
```

Config is stored at `~/.config/olmon/config.json`:

```json
{
  "host": "http://localhost:11434",
  "interval": 2,
  "no_color": false,
  "default_sort": "name"
}
```

---

## Update & Uninstall

```bash
olmon update      # update to latest version
olmon uninstall   # remove olmon and config
```

---

## Why olmon?

Most Ollama monitoring tools are GUI or system tray apps. `olmon` is built for:

- **Headless Linux servers** — no GUI required
- **Remote monitoring** — works over SSH
- **Shell scripting** — pipe-friendly with `--json` flag and exit codes
- **DevOps workflows** — integrate into scripts and cron jobs

---


## GPU Support

- **NVIDIA** — full VRAM monitoring via `nvidia-smi`
- **AMD** — coming soon
- **CPU only** — VRAM stats not available

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full plan.

---

## Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

Made with ❤️ by [Vlad Digori](https://github.com/glemiu6)