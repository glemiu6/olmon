import time

from rich.live import Live
from rich.table import Table
from rich.console import Console
from olmon.client import get_running,get_models,get_version
from olmon.config import OlmonConfig
from olmon.display import print_error, format_size

console = Console()


def _build_dashboard(resolved_host:str):
    version_data = get_version(resolved_host)
    models_data = get_models(resolved_host)
    running_data = get_running(resolved_host)

    if version_data is None:
        table=Table(title="🔴 Ollama Unreachable")
        return table
    running = running_data.get("models",[]) if running_data else []
    total = len(models_data.get("models",[])) if models_data else 0

    indicator = "🟢" if running else "🔵"
    table = Table(
        title=f"{indicator} Ollama v{version_data['version']} - {total} models installed, {len(running)} running"  # noqa: E501
    )
    table.add_column("Name")
    table.add_column("Size")
    table.add_column("VRAM")
    table.add_column("Expires At")

    for model in running:
        table.add_row(
            model.get("name","N/A"),
            format_size(model.get("size",0)),
            format_size(model.get("size_vram",0)),
            model.get("expires_at","N/A")
        )
    return table





def watch_command(host:str|None=None,
                  interval:int|None =None):
    config= OlmonConfig.load()
    resolved_host = host or config.host
    resolved_interval = interval or config.interval

    console.print(f"[dim]Watching {resolved_host} every {resolved_interval}s - Ctrl+C to stop[/dim]")  # noqa: E501
    try:
        with Live(refresh_per_second=1) as live:
            while True:
                live.update(_build_dashboard(resolved_host))
                time.sleep(resolved_interval)
    except KeyboardInterrupt:
        console.print("\n[dim]Stopping watch...[/dim]")