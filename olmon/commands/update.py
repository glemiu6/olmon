# olmon/commands/update.py
import importlib.metadata
import subprocess
import sys

from rich.console import Console

from olmon import __version__

console = Console()


def _get_latest_version() -> str | None:
    import httpx

    try:
        response = httpx.get(
            "https://api.github.com/repos/glemiu6/olmon/releases/latest", timeout=2
        )
        return response.json()["tag_name"].lstrip("v")
    except Exception:
        pass
    try:
        response = httpx.get("https://pypi.org/pypi/olmon/json", timeout=2)
        return response.json()["info"]["version"]
    except Exception:
        return None


def check_for_update() -> None:
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


def _detect_install_method() -> str:
    import os

    # PyInstaller binary
    if getattr(sys, "frozen", False):
        return "binary"

    # check if running from a known binary location
    executable = os.path.realpath(sys.argv[0])
    binary_paths = ["/usr/local/bin", "/opt/homebrew/bin", os.path.expanduser("~/.local/bin")]
    if any(executable.startswith(p) for p in binary_paths):
        return "binary"

    # pip install
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
        console.print(f"\n[bold yellow]Updating to v{latest}...[/bold yellow]")
        console.print("[dim]    Use: olmon update[/dim]\n")
        method = _detect_install_method()
        match method:
            case "pip":
                console.print("Detected pip installation, updating...")
                if importlib.util.find_spec("pip") is None:
                    console.print("pip not found, installing...")
                    subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "olmon", "--upgrade"], check=True
                )
            case "binary":
                console.print("Detected binary installation, updating...")
                result = subprocess.run(
                    [
                        "curl",
                        "-fsSL",
                        "https://raw.githubusercontent.com/glemiu6/olmon/master/scripts/install.sh",
                    ],
                    capture_output=True,
                    check=True,
                )
                subprocess.run(["bash"], input=result.stdout, check=True)
            case _:
                console.print("Unknown installation method, please update manually")
                console.print(" [cyan]pip install olmon --upgrade[/cyan]")
                console.print(
                    " [cyan]curl -fsSL https://raw.githubusercontent.com/glemiu6/olmon/master/scripts/install.sh | sh[/cyan]"  # noqa: E501
                )  # noqa: E501
        console.print(
            "[bold green]Update complete! Restart your terminal to use the latest version.[/bold green]"  # noqa: E501
        )
    except Exception as e:
        console.print(f"[bold red]Failed to update: {e}[/bold red]")
        sys.exit(1)
