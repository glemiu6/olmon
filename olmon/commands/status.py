import sys

from olmon import client, display
from olmon.config import OlmonConfig


def status_command(host:str|None =None):
    config = OlmonConfig.load()

    resolved_host = host or config.host
    version = client.get_version(resolved_host)
    
    if version is None:
        display.print_offline(resolved_host)
        sys.exit(1)

    models = client.get_models(resolved_host)
    running = client.get_running(resolved_host)

    display.print_status(
        version=version["version"],
        host=host,
        total_models = len(models["models"]),
        running_models = len(running["models"])
    )