from olmon.client import get_running
from olmon.config import OlmonConfig
from olmon.display import print_error, print_offline, print_ps_table


def ps_command(host:str|None =None):
    config = OlmonConfig.load()
    resolved_host = host or config.host
    raw = get_running(resolved_host)
    if raw is None:
        print_offline(resolved_host)
        return
    models = raw.get("models",[])

    if not models:
        print_error("No models are running")
        return
    print_ps_table(models)
