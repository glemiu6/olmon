import httpx


def get_version(host: str) -> dict | None:
    """Fetches the version information of the Ollama API"""
    try:
        response = httpx.get(f"{host}/api/version", timeout=5)
        return response.json()
    except Exception:
        return None


def get_models(host: str) -> dict | None:
    """Fetches the list of the local models available via Ollama API"""
    try:
        response = httpx.get(f"{host}/api/tags", timeout=5)
        return response.json()
    except Exception:
        return None


def get_running(host: str) -> dict | None:
    """Fetches the running models via Ollama API"""
    try:
        response = httpx.get(f"{host}/api/ps", timeout=5)
        return response.json()
    except Exception:
        return None


def get_model_info(host: str, model_name: str) -> dict | None:
    """Fetches the information of a specific model via Ollama API"""
    try:
        response = httpx.post(f"{host}/api/show", json={"model": model_name}, timeout=5)
        return response.json()
    except Exception:
        return None


def stop_model(host: str, model_name: str) -> dict | None:
    """Unloads a model from VRAM via Ollama API"""
    try:
        response = httpx.post(
            f"{host}/api/generate", json={"model": model_name, "keep_alive": 0}, timeout=5
        )
        return response.json()
    except Exception:
        return None


def get_total_vram() -> int | None:
    import platform

    if platform.system() == "Darwin":
        return _get_mac_vram()
    return _get_nvidia_vram()


def _get_nvidia_vram() -> int | None:
    try:
        import subprocess

        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            check=True,
        )
        return int(result.stdout.strip()) * 1024 * 1024
    except Exception:
        return None


def _get_mac_vram() -> int | None:
    import subprocess

    try:
        wired_limit_mb = int(
            subprocess.run(
                ["sysctl", "-n", "iogpu.wired_limit_mb"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        )
        if wired_limit_mb > 0:
            return wired_limit_mb * 1024 * 1024  # user has set a custom limit

        total_ram = int(
            subprocess.run(
                ["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, check=True
            ).stdout.strip()
        )
        return int(total_ram * 0.75)  # default policy estimate
    except Exception:
        return None

