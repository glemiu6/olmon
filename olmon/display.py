from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def print_status(version:str,host:str,total_models:int,running_models:int)->None:
    status_color = "green" if running_models>0 else "blue"
    indicator = "🟢" if running_models > 0 else "🔵"

    content = (
        f"[bold]Version[/bold] {version}\n"
        f"[bold]Host[/bold] {host}\n"
        f"[bold]Models[/bold] {total_models} installed, {running_models} running\n"
    )
    console.print(Panel(
        content,
        title=f"{indicator} Ollama is running",
        border_style=status_color
    ))

def print_models_table(models)->None:
    table = Table(title="Models")
    table.add_column("Name")
    table.add_column("Size")
    table.add_column("Params")
    table.add_column("Quantization")
    table.add_column("Format")
    for model in models:
        table.add_row(model["name"],
                      format_size(model["size"]),
                      model["details"].get("parameter_size", "N/A"),
                      model["details"].get("quantization_level","N/A"),
                      model["details"].get("format","N/A"))
    console.print(table)
def print_ps_table(processes):
    pass

def print_error(msg:str)->None:
    console.print(f"[bolt red]🔴 Error:[/bold red] {msg}")

def print_offline(host:str)->None:
    status_color = "red"
    indicator = "🔴"
    content = (
        f"[bold]Host[/bold] {host}\n\n"
        f"Make sure Ollama is running:\n"
        f"[bold yellow]ollama serve[/bold yellow]\n"
    )
    console.print(Panel(
        content,
        title=f"{indicator} Ollama is unreachable",
        border_style=status_color
    ))

def format_size(bts:int)->str:
    gb = bts / (1024**3)
    if gb>=1:
        return f"{gb:.1f} GB"
    mb= bts / (1024**2)
    return f"{mb:.1f} MB"