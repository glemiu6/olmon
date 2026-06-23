#olmon/commands/update.py
import json
import subprocess
import sys
from rich.console import Console
from olmon import __version__

def _get_latest_version()->str|None:
    import urllib.request
    try:
        with urllib.request.urlopen("https://api.github.com/repos/glemiu6/olmon/releases/latest",timeout=2) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data["tag_name"].lstrip("v")
    except Exception:
        return None

