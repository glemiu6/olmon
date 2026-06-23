from olmon.config import OlmonConfig
from olmon.display import print_error, print_offline


def models_command(host:str|None =None,
                   sort:str|None =None,
                   filters:str|None =None):
    from olmon.client import get_models
    from olmon.display import print_models_table

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
    
def inspect_command(host: str | None =None, model: str | None =None):
    from olmon.client import get_model_info
    from olmon.display import print_inspect
    config = OlmonConfig.load()
    resolved_host = host or config.host
    raw = get_model_info(resolved_host,model)
    if raw is None:
        print_error(f"Could not find info for '{model}'")
        return
    print_inspect(raw)

    