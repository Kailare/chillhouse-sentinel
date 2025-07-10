import json
from typing import Any, Dict


def notify(alert: str, token: Dict[str, Any]) -> None:
    payload = {"alert": alert, "token": token}
    print(json.dumps(payload, ensure_ascii=True))
