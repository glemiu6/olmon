#olmon/config.py
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from platformdirs import user_config_dir

CONFIG_PATH = Path(user_config_dir("olmon")) / "config.json"

@dataclass
class OlmonConfig:
    host:str = "http://localhost:11434"
    interval:int = 2
    no_color:bool = False
    default_sort:str = "name"

    @classmethod
    def load(cls):
        if not CONFIG_PATH.exists():
            return cls()
        with open(CONFIG_PATH,"r") as f:
            data = json.load(f)

        return cls(**{
            k:v for k,v in data.items()
            if k in cls.__dataclass_fields__
        })

    def save(self):
        CONFIG_PATH.parent.mkdir(parents=True,exist_ok=True)
        with open(CONFIG_PATH,"w") as f:
            json.dump(asdict(self),f,indent=2)