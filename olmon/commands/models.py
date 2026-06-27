import sys

from olmon.config import OlmonConfig
from olmon.display import print_error, print_offline


def models_command(host: str | None = None, sort: str | None = None, filters: str | None = None,json_output: bool = False):
    from olmon.client import get_models
    from olmon.display import print_models_table

    config = OlmonConfig.load()
    resolved_host = host or config.host
    raw = get_models(resolved_host)
    if raw is None:
        print_offline(resolved_host)
        sys.exit(1)
    if "models" not in raw:
        print_error("unexpected response from Ollama API")
        sys.exit(2)
    models = raw["models"]
    if json_output:
        import json
        print(json.dumps(models, indent=2))
        sys.exit(0)

    if filters:
        models = [m for m in models if filters.lower() in m["name"].lower()]
    sort_key = sort or config.default_sort
    if sort_key == "size":
        models = sorted(models, key=lambda x: x["size"], reverse=True)
    elif sort_key == "date":
        models = sorted(models, key=lambda x: x["modified_at"], reverse=True)
    else:
        models = sorted(models, key=lambda x: x["name"])

    print_models_table(models)
    sys.exit(0)


def inspect_command(host: str | None = None, name: str | None = None):
    from olmon.client import get_model_info
    from olmon.display import print_inspect

    config = OlmonConfig.load()
    resolved_host = host or config.host

    if name is None:  # ← guard against None before passing to client
        print_error("Model name is required")
        sys.exit(1)

    data = get_model_info(resolved_host, name)

    if data is None:
        print_error(f"Could not fetch info for '{name}'")
        sys.exit(1)

    print_inspect(data)
