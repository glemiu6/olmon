import time

from rich.console import Console
from rich.live import Live
from rich.table import Table

from olmon.client import get_models, get_running, get_total_vram, get_version
from olmon.config import OlmonConfig
from olmon.display import format_size

console = Console()


def _build_dashboard(resolved_host: str, total_vram: int | None):
    version_data = get_version(resolved_host)
    models_data = get_models(resolved_host)
    running_data = get_running(resolved_host)

    if version_data is None:
        table = Table(title="🔴 Ollama Unreachable")
        return table
    running = running_data.get("models", []) if running_data else []
    total = len(models_data.get("models", [])) if models_data else 0

    indicator = "🟢" if running else "🔵"
    title = f"{indicator} Ollama v{version_data['version']} - {total} models installed, {len(running)} running"  # noqa: E501
    if total_vram:
        used_vram = sum(m.get("size_vram", 0) for m in running)
        if used_vram / total_vram >= 0.9:
            title += " ⚠ VRAM above 90%"
    table = Table(title=title)

    table.add_column("Name")
    table.add_column("Size")
    table.add_column("VRAM")
    table.add_column("Expires At")

    for model in running:
        table.add_row(
            model.get("name", "N/A"),
            format_size(model.get("size", 0)),
            format_size(model.get("size_vram", 0)),
            model.get("expires_at", "N/A"),
        )
    return table


def watch_command(host: str | None = None, interval: int | None = None):
    config = OlmonConfig.load()
    resolved_host = host or config.host
    resolved_interval = interval or config.interval
    total_vram = get_total_vram()

    console.print(
        f"[dim]Watching {resolved_host} every {resolved_interval}s - Ctrl+C to stop[/dim]"
    )  # noqa: E501
    try:
        with Live(refresh_per_second=1) as live:
            while True:
                live.update(_build_dashboard(resolved_host, total_vram))
                time.sleep(resolved_interval)
    except KeyboardInterrupt:
        console.print("\n[dim]Stopping watch...[/dim]")
