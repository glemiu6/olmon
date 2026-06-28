import sys

from olmon.client import get_model_info
from olmon.config import OlmonConfig
from olmon.display import print_compare, print_error


def compare_command(host: str | None = None, models: list[str] | None = None) -> None:

    config = OlmonConfig.load()
    resolved_host = host or config.host

    if models is None or len(models) < 2:
        print_error("Please provide at least 2 models to compare")
        sys.exit(2)
    results = {}
    for name in models:
        data = get_model_info(resolved_host, name)
        if data is None:
            print(f"Could not find info for '{name}'")
            sys.exit(1)
        results[name] = data

    print_compare(results)
