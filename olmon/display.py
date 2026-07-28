import datetime
import time

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from olmon.db import estimate_vram_bytes

console = Console()


def print_status(
    version: str, host: str, total_models: int, running_models: int, vram_used: str
) -> None:  # noqa: E501
    status_color = "green" if running_models > 0 else "blue"
    indicator = "🟢" if running_models > 0 else "🔵"

    content = (
        f"[bold]Version[/bold] {version}\n"
        f"[bold]Host[/bold] {host}\n"
        f"[bold]Models[/bold] {total_models} installed, {running_models} running\n"
        f"[bold]VRAM[/bold] {vram_used} \n"
    )
    console.print(Panel(content, title=f"{indicator} Ollama is running", border_style=status_color))


def print_models_table(models) -> None:
    table = Table(title="Models")
    table.add_column("Name")
    table.add_column("Size")
    table.add_column("Params")
    table.add_column("Quantization")
    table.add_column("Format")
    for model in models:
        table.add_row(
            model["name"],
            format_size(model["size"]),
            model["details"].get("parameter_size", "N/A"),
            model["details"].get("quantization_level", "N/A"),
            model["details"].get("format", "N/A"),
        )
    console.print(table)


def print_ps_table(processes) -> None:
    table = Table(title="Running Models")
    table.add_column("Name")
    table.add_column("Size")
    table.add_column("VRAM")
    table.add_column("Params")
    table.add_column("Context Length")
    table.add_column("Family")
    table.add_column("Quantization")
    table.add_column("Expires At")

    for model in processes:
        table.add_row(
            model.get("name", "N/A"),
            format_size(model.get("size", 0)),
            format_size(model.get("size_vram", 0)),
            model.get("details", {}).get("parameter_size", "N/A"),
            str(model.get("context_length", 0)),
            model.get("details", {}).get("family", "N/A"),
            model.get("details", {}).get("quantization_level", "N/A"),
            model.get("expires_at", "N/A"),
        )
    console.print(table)


def print_error(msg: str) -> None:
    console.print(f"[bold red]🔴 Error:[/bold red] {msg}")


def print_offline(host: str) -> None:
    status_color = "red"
    indicator = "🔴"
    content = (
        f"[bold]Host[/bold] {host}\n\n"
        f"Make sure Ollama is running:\n"
        f"[bold yellow]ollama serve[/bold yellow]\n"
    )
    console.print(
        Panel(content, title=f"{indicator} Ollama is unreachable", border_style=status_color)
    )


def print_inspect(data: dict):
    details = data.get("details", {})
    model_info = data.get("model_info", {})
    capabilities = data.get("capabilities", [])

    raw_params = data.get("parameters", "")
    params = {}
    for line in raw_params.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            params[parts[0]] = parts[1]

    modified = data.get("modified_at", "—").split("T")[0]

    # find context_length from model_info (key ends with .context_length)
    context = next((str(v) for k, v in model_info.items() if k.endswith(".context_length")), "—")
    embedding = next(
        (str(v) for k, v in model_info.items() if k.endswith(".embedding_length")), "—"
    )
    blocks = next((str(v) for k, v in model_info.items() if k.endswith(".block_count")), "—")

    content = (
        f"[bold]Family[/bold]         {details.get('family', '—')}\n"
        f"[bold]Format[/bold]         {details.get('format', '—')}\n"
        f"[bold]Parameters[/bold]     {details.get('parameter_size', '—')}\n"
        f"[bold]Quantization[/bold]   {details.get('quantization_level', '—')}\n"
        f"[bold]Modified[/bold]       {modified}\n"
        f"[bold]Capabilities[/bold]   {', '.join(capabilities) if capabilities else '—'}\n"
        f"\n"
        f"[bold]Context[/bold]        {context} tokens\n"
        f"[bold]Embedding[/bold]      {embedding}\n"
        f"[bold]Blocks[/bold]         {blocks}\n"
        f"[bold]Temperature[/bold]    {params.get('temperature', '—')}\n"
        f"[bold]num_ctx[/bold]        {params.get('num_ctx', '—')}\n"
    )

    console.print(Panel(content, title=f"[bold]{details.get('family', 'Model')}[/bold]"))


def print_stop(model: str) -> None:
    console.print(f"[bold green]✓[/bold green] {model} unloaded from VRAM")


def print_recommend(tags, max_bytes: int) -> None:
    table = Table(title=f"Models with an estimated VRAM need under {format_size(max_bytes)}")
    table.add_column("Model")
    table.add_column("File Size")
    table.add_column("Est. VRAM")
    table.add_column("Context")
    table.add_column("Pulls")

    for tag in tags:
        table.add_row(
            tag["full_name"],
            format_size(tag["size_bytes"]),
            f"~{format_size(estimate_vram_bytes(tag['size_bytes']))}",
            str(tag["context_length"] or "—"),
            format_pulls(tag["pulls"]),
        )
    console.print(table)
    console.print(
        "[dim]Est. VRAM includes a rough margin for KV cache/compute overhead beyond file size[/dim]"  # noqa: E501
    )


def print_fit(model: str, size_bytes: int, total_vram: int, source: str, fits: bool) -> None:
    estimated = estimate_vram_bytes(size_bytes)
    indicator, color = ("✓", "green") if fits else ("✗", "red")
    verdict = "fits" if fits else "does not fit"
    console.print(
        f"[{color}]{indicator}[/{color}] {model} {verdict} — "
        f"file size {format_size(size_bytes)}, [dim]est. VRAM ~{format_size(estimated)}[/dim] "
        f"/ {format_size(total_vram)} VRAM [dim]({source})[/dim]"
    )


def print_stop_error(model: str) -> None:
    console.print(f"[bold red]✗[/bold red] Could not unload {model} from VRAM")


def print_compare(models: dict):
    table = Table(title="Model Comparison")
    table.add_column("", style="bold")

    for name in models:
        table.add_column(name, justify="center")

    def get_info(data, key):
        return next((str(v) for k, v in data.get("model_info", {}).items() if k.endswith(key)), "—")

    fields = [
        ("Family", lambda d: d.get("details", {}).get("family", "—")),
        ("Format", lambda d: d.get("details", {}).get("format", "—")),
        ("Parameters", lambda d: d.get("details", {}).get("parameter_size", "-")),
        ("Quantization", lambda d: d.get("details", {}).get("quantization_level", "-")),
        ("Context", lambda d: get_info(d, key=".context_length")),
        ("Embedding", lambda d: get_info(d, key=".embedding_length")),
        ("Blocks", lambda d: get_info(d, key=".block_count")),
    ]

    for label, extractor in fields:
        row = [label] + [extractor(data) for data in models.values()]
        table.add_row(*row)
    console.print(table)


def print_top(models: list, total_vram: int | None) -> Panel:
    used_vram = sum(m.get("size_vram", 0) for m in models)

    if total_vram:
        pct = used_vram / total_vram
        vram_summary = f"VRAM: {format_size(used_vram)} / {format_size(total_vram)}"
        if pct >= 0.9:
            vram_summary += "   [bold red]⚠ VRAM above 90%[/bold red]"
    else:
        vram_summary = f"VRAM: {format_size(used_vram)} used"

    header = f"{vram_summary} |  {len(models)} running"

    table = Table(box=None, pad_edge=False, show_header=True, expand=True)
    table.add_column("Model", style="bold", min_width=20)
    table.add_column("VRAM", min_width=12)
    table.add_column("VRAM %", min_width=12)
    table.add_column("Expires In", min_width=10)
    table.add_column("Status", min_width=12)

    for model in models:
        name = model.get("name", "-")
        size_vram = model.get("size_vram", 0)
        expires_at = model.get("expires_at", "-")

        countdown = format_countdown(expires_at)
        vram_bar = format_vram_bar(size_vram, total_vram)

        try:
            expires = datetime.datetime.fromisoformat(expires_at)
            remaining = (expires - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
            status = "[green]● active[/green]" if remaining > 60 else "[yellow]● expiring[/yellow]"
        except Exception:
            status = "[green]● active[/green]"

        table.add_row(
            name,
            format_size(size_vram),
            vram_bar,
            countdown,
            status,
        )

    return Panel(
        table,
        title=f"[bold]olmon top[/bold] [dim]{datetime.datetime.now().strftime('%H:%M:%S')}[/dim]",
        subtitle=header,
        width=min(console.width, 100),
    )


def run_top(host: str, interval: int, total_vram: int | None):
    from olmon.client import get_running

    try:
        with Live(refresh_per_second=1, transient=True) as live:
            while True:
                raw = get_running(host)
                models = raw.get("models", []) if raw else []
                live.update(print_top(models, total_vram))
                time.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n[dim]Stopped.[/dim]")


def print_search_results(rows, query: str) -> None:
    if not rows:
        console.print(f"[yellow]No cached models match '{query}'[/yellow] — try: olmon db update")
        return

    table = Table(title=f"Search results for '{query}'")
    table.add_column("Model")
    table.add_column("Description", max_width=50)
    table.add_column("Capabilities")
    table.add_column("Tags", justify="right")
    table.add_column("Pulls", justify="right")

    for row in rows:
        table.add_row(
            row["name"],
            row["description"] or "—",
            row["capabilities"].replace(",", ", ") if row["capabilities"] else "—",
            str(row["tag_count"]),
            format_pulls(row["pulls"]),
        )
    console.print(table)
    console.print(f"[dim]{len(rows)} result(s)[/dim]")


def format_pulls(pulls: int) -> str:
    if pulls >= 1_000_000:
        return f"{pulls / 1_000_000:.1f}M"
    if pulls >= 1_000:
        return f"{pulls / 1_000:.1f}K"
    return str(pulls)


def format_size(bts: int) -> str:
    gb = bts / (1024**3)
    if gb >= 1:
        return f"{gb:.1f} GB"
    mb = bts / (1024**2)
    return f"{mb:.1f} MB"


def format_countdown(expires_at: str) -> str:
    try:
        expires = datetime.datetime.fromisoformat(expires_at)
        remaining = expires - datetime.datetime.now(datetime.timezone.utc)
        total_sec = int(remaining.total_seconds())
        if total_sec <= 0:
            return "expiring..."
        mins, secs = divmod(total_sec, 60)
        return f"{mins}m {secs}s"
    except Exception:
        return "-"


def format_vram_bar(used: int, total: int | None) -> str:
    if total is None:
        return "— " * 5  # consistent width
    pct = min(used / total, 1.0)  # ← cap at 100% to avoid overflow
    filled = int(pct * 5)
    bar = "█" * filled + "░" * (5 - filled)
    return f"{bar} {int(pct * 100):>3}%"
