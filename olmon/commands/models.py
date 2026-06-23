from olmon.client import get_models
from olmon.config import OlmonConfig
from olmon.display import print_error, print_models_table, print_offline


def models_command(host:str=None,
                   sort:str=None,
                   filters:str=None):
    config = OlmonConfig.load()
    resolved_host = host or config.host
    raw = get_models(resolved_host)
    if raw is None:
        print_offline(resolved_host)
        return
    if "models" not in raw:
        print_error("unexpected response from Ollama API")
    models = raw["models"]

    if filters:
        models = [m for m in models if filters.lower() in m["name"].lower()]
    sort_key = sort or config.default_sort
    if sort_key == "size":
        models = sorted(models,key=lambda x:x["size"],reverse=True)
    elif sort_key == "date":
        models = sorted(models,key=lambda x:x["modified_at"],reverse=True)
    else:
        models = sorted(models,key=lambda x:x["name"])

    print_models_table(models)