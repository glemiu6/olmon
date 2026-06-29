import sys

from olmon.client import get_running, get_total_vram
from olmon.config import OlmonConfig
from olmon.display import print_offline, run_top


def top_command(host: str | None = None, interval: int | None = None):
    config = OlmonConfig.load()
    resolved_host = host or config.host
    resolved_interval = interval or config.interval

    total_vram = get_total_vram()

    if get_running(resolved_host) is None:
        print_offline(resolved_host)
        sys.exit(1)

    run_top(resolved_host, resolved_interval, total_vram)
    sys.exit(0)
