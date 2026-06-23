#olmon/commands/update.py
import importlib.metadata
import json
import subprocess
import sys

from rich.console import Console

from olmon import __version__

console = Console()

def _get_latest_version() -> str | None:
    import urllib.request

    for url, extract in [
        (
            "https://api.github.com/repos/glemiu6/olmon/releases/latest",
            lambda d: d["tag_name"].lstrip("v"),
        ),
        (
            "https://pypi.org/pypi/olmon/json",
            lambda d: d["info"]["version"],
        ),
    ]:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                return extract(json.loads(r.read().decode("utf-8")))
        except Exception:
            continue

    return None


def check_for_update()->None:
    try:
        latest_version = _get_latest_version()
        if latest_version is None:
            return
        if latest_version != __version__:
            console.print(
                f"\n[bold yellow]!! New version available: v{latest_version}[/bold yellow] [dim](you have v{__version__})[/dim]"  # noqa: E501
            )
            console.print("[dim]    Use: olmon update[/dim]\n")
    except Exception:
        pass



def _detect_install_method()->str:
    if getattr(sys, "frozen", False):
        return "binary"

    try:
        importlib.metadata.version("olmon")
        return "pip"
    except importlib.metadata.PackageNotFoundError:
        pass

    return "binary"



def update():
    try:
        import importlib.util

        latest = _get_latest_version()
        if latest is None:
            return
        if latest == __version__:
            console.print("[bold green]Already up to date[/bold green]")
            return
        console.print(
            f"\n[bold yellow]!! New version available: v{latest}[/bold yellow] [dim](you have v{__version__})[/dim]"  # noqa: E501
            )
        console.print("[dim]    Use: olmon update[/dim]\n")
        method = _detect_install_method()
        match method:
            case "pip":
                console.print("Detected pip installation, updating...")
                if importlib.util.find_spec("pip") is None:
                    console.print("pip not found, installing...")
                    subprocess.run([sys.executable,"-m","ensurepip","--upgrade"],check=True)
                subprocess.run(
                    [sys.executable,"-m","pip","install","olmon","--upgrade"],
                    check=True
                )
            case "binary":
                console.print("Detected binary installation, updating...")
                result = subprocess.run(
                        [
                            "curl",
                            "-fsSL",
                            "https://raw.githubusercontent.com/glemiu6/olmon/master/scripts/install.sh"
                        ],
                        capture_output=True,
                        check=True
                )
                subprocess.run(["bash"],input=result.stdout,check=True)
            case _:
                console.print("Unknown installation method, please update manually")
                console.print(" [cyan]pip install olmon --upgrade[/cyan]")
                console.print(" [cyan]curl -fsSL https://raw.githubusercontent.com/glemiu6/olmon/master/scripts/install.sh | sh[/cyan]")  # noqa: E501
        console.print(
            "[bold green]Update complete! Restart your terminal to use the latest version.[/bold green]"  # noqa: E501
        )
    except Exception as e:
        console.print(f"[bold red]Failed to update: {e}[/bold red]")
        sys.exit(1)