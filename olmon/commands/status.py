import sys

from olmon.client import get_models, get_running, get_total_vram, get_version
from olmon.config import OlmonConfig
from olmon.display import format_size, print_offline, print_status


def status_command(host: str | None = None):
    config = OlmonConfig.load()
    resolved_host = host or config.host

    version_data = get_version(resolved_host)
    if version_data is None:
        print_offline(resolved_host)
        sys.exit(1)

    models_data = get_models(resolved_host)
    running_data = get_running(resolved_host)

    total = len(models_data["models"]) if models_data else 0
    models_list = running_data.get("models", []) if running_data else []
    running = len(models_list)

    vram_used = sum(m.get("size_vram", 0) for m in models_list)
    total_vram = get_total_vram()

    if total_vram:
        stat_vram = f"{format_size(vram_used)} / {format_size(total_vram)}"
    else:
        stat_vram = format_size(vram_used)

    print_status(
        version=version_data["version"],
        host=resolved_host,
        total_models=total,
        running_models=running,
        vram_used=stat_vram,
    )
    sys.exit(0)
