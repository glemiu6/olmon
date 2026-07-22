import sys

from olmon.client import get_models, get_total_vram
from olmon.config import OlmonConfig
from olmon.db import get_connection, get_tags_for_model
from olmon.display import print_error, print_fit


def fit_command(host:str|None=None,model:str|None=None)->None:
    if not model:
        print_error("Model name is required")
        sys.exit(2)

    config = OlmonConfig.load()
    resolved_host= host or config.host
    total_vram=get_total_vram()
    if total_vram is None:
        print_error("Could not fetch total VRAM")
        sys.exit(2)

    installed = get_models(resolved_host)
    if installed is None:
        print_error("Could not fetch installed models")
    installed_models = installed.get("models", []) if installed else []
    matchs = next(
        (m for m in installed_models if m["name"] in (model,f"{model}:latest")), None
    )

    if matchs:
        size_bytes = matchs["size"]
        source = f"installed ({matchs['name']})"
    else:
        base_name,_,tag = model.partition(":")
        conn = get_connection()
        tags = get_tags_for_model(conn, base_name)
        conn.close()
        found = (
            next((f for f in tags if f["tag"]==tag),None)
            if tag
            else next((t for t in tags if t["is_default"]),None)
        )
        if not found or found["size_bytes"] is None:
            print_error(f"'{model}' not found — try: olmon db update")
            sys.exit(2)
        size_bytes = found["size_bytes"]
        source = f"cached ({found["full_name"]})"

    fits = size_bytes <= total_vram
    print_fit(model, size_bytes, total_vram, source, fits)
    sys.exit(0 if fits else 1)