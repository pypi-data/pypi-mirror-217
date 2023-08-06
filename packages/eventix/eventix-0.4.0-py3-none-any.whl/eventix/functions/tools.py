import datetime
import json
from uuid import uuid4

import psutil


def uid() -> str:
    return str(uuid4()).replace("-", "")


_uid = uid


def metrics() -> dict:
    memory_info = psutil.Process().memory_info()
    return {
        "memory": dict(rss=memory_info.rss, vms=memory_info.vms, data=memory_info.data)
    }

