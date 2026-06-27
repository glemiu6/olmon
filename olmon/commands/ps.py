import sys

from olmon.client import get_running,stop_model
from olmon.config import OlmonConfig
from olmon.display import print_error, print_offline, print_ps_table,print_stop_error,print_stop


def ps_command(host: str | None = None):
    config = OlmonConfig.load()
    resolved_host = host or config.host
    raw = get_running(resolved_host)
    if raw is None:
        print_offline(resolved_host)
        sys.exit(1)
    models = raw.get("models", [])

    if not models:
        print_error("No models are running")
        sys.exit(2)
    print_ps_table(models)
    sys.exit(0)

def stop_command(host: str | None = None,model_name: str | None = None) -> None:
    config = OlmonConfig.load()
    resolved_host = host or config.host

    if model_name is None:
        print_error("Model name is required")
        sys.exit(2)
    raw = stop_model(resolved_host, model_name)
    if raw is None:
        print_stop_error(model_name)
        sys.exit(1)
    print_stop(model_name)
    sys.exit(0)

