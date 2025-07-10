import asyncio
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

import websockets
from dotenv import load_dotenv

from engine.brain import AgentBrain
from engine.notifier import notify
from engine.warning_generator import WarningGenerator

PUMPPORTAL_WS_URL = "wss://pumpportal.fun/api/data"


@dataclass
class AgentState:
    last_token: Optional[Dict[str, Any]] = None
    last_alert: Optional[str] = None
    detection_count: int = 0


class ChillhouseAgent:
    def __init__(self) -> None:
        self.brain = AgentBrain()
        self.fallback = WarningGenerator()
        self.state = AgentState()

    @staticmethod
    def _contains_chillhouse(token: Dict[str, Any]) -> bool:
        name = str(token.get("name", ""))
        symbol = str(token.get("symbol", ""))
        target = "chillhouse"
        return target in name.lower() or target in symbol.lower()

    @staticmethod
    def _format_token_summary(token: Dict[str, Any]) -> str:
        name = token.get("name", "unknown")
        symbol = token.get("symbol", "unknown")
        mint = token.get("mint", "unknown")
        return f"{name} ({symbol}) | mint={mint}"

    async def decide(self, token: Dict[str, Any]) -> Optional[str]:
        if not self._contains_chillhouse(token):
            return None

        alert = await self.brain.analyze_risk(token)
        if alert:
            return alert

        summary = self._format_token_summary(token)
        name = str(token.get("name", "unknown"))
        mint = str(token.get("mint", "unknown"))
        return self.fallback.generate(summary=summary, name=name, mint=mint)

    def act(self, token: Dict[str, Any], alert: str) -> None:
        self.state.last_token = token
        self.state.last_alert = alert
        self.state.detection_count += 1
        notify(alert, token)


async def _listen() -> None:
    agent = ChillhouseAgent()
    async with websockets.connect(PUMPPORTAL_WS_URL) as websocket:
        subscribe_payload = {"method": "subscribeNewToken"}
        await websocket.send(json.dumps(subscribe_payload))
        print("Agent active. Monitoring pump.fun...")

        async for raw_message in websocket:
            try:
                message = json.loads(raw_message)
            except json.JSONDecodeError:
                print("Skipping non-JSON message")
                continue

            token = message.get("data", {}) if isinstance(message, dict) else {}
            if not isinstance(token, dict):
                continue

            alert = await agent.decide(token)
            if alert:
                agent.act(token, alert)
                print(f"Alert #{agent.state.detection_count} dispatched.")


def main() -> None:
    load_dotenv()
    asyncio.run(_listen())


if __name__ == "__main__":
    main()
