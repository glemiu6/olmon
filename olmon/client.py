import requests


def get_version()->dict|None:
    """
    Fetches the version information of the Ollama API
    """
    try:
        result = requests.get("http://localhost:11434/api/version")
        return result.json()
    except requests.ConnectionError:
        return None

def get_models()->dict|None:
    """
    Fetches the list of the local models available via Ollama API
    """
    try:
        result = requests.get("http://localhost:11434/api/tags")
        return result.json()
    except requests.ConnectionError:
        return None

def get_running():
    """
    Fetches the running models running via Ollama API
    """
    try:
        result = requests.get("http://localhost:11434/api/ps")
        return result.json()
    except requests.ConnectionError:
        return None

def get_model_info(model_name:str)->dict|None:
    """
     Fetches the information of a specific model via Ollama API
    """
    try:
        result = requests.post("http://localhost:11434/api/show",json={"model":model_name})
        return result.json()
    except requests.ConnectionError:
        return None
