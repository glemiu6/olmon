from olmon.client import get_models


def models_command():
    raw = get_models()
    models = raw["model"]
    models = sorted(models,key=lambda x:x["name"])
    #display models