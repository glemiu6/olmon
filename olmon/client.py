import json
import urllib.request


def get_version(host:str)->dict|None:
    """
    Fetches the version information of the Ollama API
    """
    try:
        with urllib.request.urlopen(f"{host}/api/version") as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None

def get_models(host:str)->dict|None:
    """
    Fetches the list of the local models available via Ollama API
    """
    try:
        with urllib.request.urlopen(f"{host}/api/tags") as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None

def get_running(host:str)->dict|None:
    """
    Fetches the running models running via Ollama API
    """
    try:
        with urllib.request.urlopen(f"{host}/api/ps") as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None

def get_model_info(host:str,model_name:str)->dict|None:
    """
     Fetches the information of a specific model via Ollama API
    """
    try:
        data = json.dumps({"model":model_name}).encode("utf-8")

        req = urllib.request.Request(
            url=f"{host}/api/show",
            data=data,
            headers={"Content-Type":"application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req) as result:
            return json.loads(result.read().decode("utf-8"))
    except Exception:
        return None
