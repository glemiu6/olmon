import os

from platformdirs import user_config_dir

from olmon.config import OlmonConfig

APP_NAME = "olmon"

def get_default_config_path() -> str:
    config_dir = user_config_dir(APP_NAME)
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")


def init_config() -> None:
    paths= get_default_config_path()
    if os.path.exists(paths):
        choice = input("Config file already exists. Overwrite? (y/n): ").lower()
        if choice != "y":
            return

    host = input("Ollama host [http://localhost:11434]: ") or "http://localhost:11434"
    interval = input("Update interval [2]: ") or 2
    no_color = input("Disable color [False]: ") or False
    default_sort = input("Default sort [name]: ") or "name"

    cfg = OlmonConfig(
        host, int(interval), bool(no_color), default_sort
    )
    cfg.save()
    print("Config file created at", paths)