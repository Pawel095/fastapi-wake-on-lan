# Builtins
from typing import Optional

# 3rd party
from pydantic import BaseModel


class Target(BaseModel):
    mac: str = "74:D0:2B:91:EE:04"
    name: str = "pawel-old"
    description: Optional[str] = "Stary PC pawła"
    ip: Optional[str] = "192.168.0.147"
    broadcast: str = "192.168.0.255"
