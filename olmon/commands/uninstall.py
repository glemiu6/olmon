#olmon/commands/uninstall.py
def uninstall() -> None:
    """Remove olmon completely = pip, binary, and config."""
    import os
    import shutil
    import subprocess
    import sys

    from rich.console import Console

    console = Console()

    console.print("[bold red]Uninstalling olmon...[/bold red]")
    method = _detect_install_method()

    # Remove config file
    config_path = os.path.expanduser("~/.config/olmon")
    if os.path.exists(config_path):
        shutil.rmtree(config_path)
        console.print("[green]Removed ~/.config/olmon[/green]")

    if sys.platform == "win32":
        windows_path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "komit")
        if os.path.exists(windows_path):
            shutil.rmtree(windows_path)
            console.print(f"[green]Removed {windows_path}[/green]")
        try:
            import winreg

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
            current_path, _ = winreg.QueryValueEx(key, "Path")
            new_path = ";".join(p for p in current_path.split(";") if "komit" not in p)
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(key)
            console.print("[green]Removed from PATH[/green]")
        except Exception as e:
            console.print(f"[yellow]Could not remove from PATH: {e}[/yellow]")
    # Remove binary if installed via curl
    all_paths = ["~/.local/bin/olmon", "/usr/local/bin/olmon", "/opt/homebrew/bin/olmon"]

    for p in all_paths:
        binary = os.path.expanduser(p)
        if os.path.exists(binary):
            try:
                subprocess.run(["sudo", "rm", "-f", binary], check=True)
                console.print(f"[green]Removed {binary}[/green]")
            except subprocess.CalledProcessError:
                console.print(f"[yellow]Failed to remove {binary} - try: sudo rm {binary}[/yellow]")
    # remove for pip
    if method == "pip":
        try:
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "olmon", "-y"], check=False)
            console.print("[green]Removed pip package[/green]")
        except subprocess.CalledProcessError:
            pass

    console.print("\n[bold red]komit uninstalled. Goodbye![/bold red]")


def _detect_install_method() -> str:
    import importlib.metadata
    import sys

    # 1. PyInstaller / bundled binary
    if getattr(sys, "frozen", False):
        return "binary"

    # 2. pip install (most reliable check)
    try:
        importlib.metadata.version("olmon")
        return "pip"
    except importlib.metadata.PackageNotFoundError:
        pass

    # 3. fallback
    return "binary"