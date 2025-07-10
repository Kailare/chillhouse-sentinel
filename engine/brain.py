import asyncio
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AgentBrain:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        self.enabled = bool(api_key)
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    async def analyze_risk(self, token_data: Dict[str, Any]) -> Optional[str]:
        if not self.enabled or not self.client:
            return None

        prompt = (
            "Analyze this Solana pump.fun token launch for security risks:\n"
            f"Name: {token_data.get('name')}\n"
            f"Mint: {token_data.get('mint')}\n\n"
            "Generate a short, 1-sentence security warning focusing on either "
            "Bundling, Dev History, or Liquidity. Return ONLY the warning string "
            "starting with an emoji."
        )

        def _call() -> str:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()

        try:
            return await asyncio.to_thread(_call)
        except Exception:
            return None
