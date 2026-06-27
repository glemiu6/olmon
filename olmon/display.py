from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_status(version: str, host: str, total_models: int, running_models: int) -> None:
    status_color = "green" if running_models > 0 else "blue"
    indicator = "🟢" if running_models > 0 else "🔵"

    content = (
        f"[bold]Version[/bold] {version}\n"
        f"[bold]Host[/bold] {host}\n"
        f"[bold]Models[/bold] {total_models} installed, {running_models} running\n"
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

    # parse parameters string into a dict
    # "temperature 0.7\nnum_ctx 2048" → {"temperature": "0.7", "num_ctx": "2048"}
    raw_params = data.get("parameters", "")
    params = {}
    for line in raw_params.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            params[parts[0]] = parts[1]

    # clean up modified_at
    modified = data.get("modified_at", "—").split("T")[0]

    # find context_length from model_info (key ends with .context_length)
    context = next((str(v) for k, v in model_info.items() if k.endswith(".context_length")), "—")
    embedding = next(
        (str(v) for k, v in model_info.items() if k.endswith(".embedding_length")), "—"
    )
    blocks = next((str(v) for k, v in model_info.items() if k.endswith(".block_count")), "—")

    # build the panel content
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


def print_stop_error(model: str) -> None:
    console.print(f"[bold red]✗[/bold red] Could not unload {model} from VRAM")


def format_size(bts: int) -> str:
    gb = bts / (1024**3)
    if gb >= 1:
        return f"{gb:.1f} GB"
    mb = bts / (1024**2)
    return f"{mb:.1f} MB"
