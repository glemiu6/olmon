import sys

from olmon import client, display
from olmon.config import OlmonConfig


def status_command(host: str | None = None):
    config = OlmonConfig.load()
    resolved_host = host or config.host

    version_data = client.get_version(resolved_host)

    if version_data is None:
        display.print_offline(resolved_host)
        sys.exit(1)

    models_data = client.get_models(resolved_host)
    running_data = client.get_running(resolved_host)

    total = len(models_data["models"]) if models_data else 0
    running = len(running_data["models"]) if running_data else 0

    display.print_status(
        version=version_data["version"],
        host=resolved_host,
        total_models=total,
        running_models=running,
    )
    sys.exit(0)
