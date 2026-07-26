import sys

from olmon.client import get_models, get_total_vram
from olmon.config import OlmonConfig
from olmon.db import estimate_vram_bytes, get_connection, get_tags_for_model
from olmon.display import print_error, print_fit


def fit_command(host: str | None = None, model_name: str | None = None) -> None:
    if not model_name:
        print_error("Model name is required")
        sys.exit(2)

    config = OlmonConfig.load()
    resolved_host = host or config.host

    total_vram = get_total_vram()
    if total_vram is None:
        print_error("Could not detect VRAM (no NVIDIA GPU found)")
        sys.exit(1)

    # installed? -> use the real size from /api/tags
    installed = get_models(resolved_host)
    installed_models = installed.get("models", []) if installed else []
    match = next(
        (m for m in installed_models if m["name"] in (model_name, f"{model_name}:latest")), None
    )

    if match:
        size_bytes = match["size"]
        source = f"installed ({match['name']})"
    else:
        # not installed -> look it up in the local ollama.com cache
        base_name, _, tag = model_name.partition(":")
        conn = get_connection()
        tags = get_tags_for_model(conn, base_name)
        conn.close()

        found = (
            next((t for t in tags if t["tag"] == tag), None)
            if tag
            else next((t for t in tags if t["is_default"]), None)
        )
        if not found or found["size_bytes"] is None:
            print_error(f"'{model_name}' not found — try: olmon db update")
            sys.exit(1)

        size_bytes = found["size_bytes"]
        source = f"cached ({found['full_name']})"

    fits = estimate_vram_bytes(size_bytes) <= total_vram
    print_fit(model_name, size_bytes, total_vram, source, fits)
    sys.exit(0 if fits else 1)
