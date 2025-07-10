import random


class WarningGenerator:
    def __init__(self) -> None:
        self.templates = [
            "Security Alert: High bundling detected. Review holder distribution. {summary}",
            "Security Alert: Dev address linked to prior failures. Proceed with caution. {summary}",
            "Security Alert: Metadata mismatch observed across sources. {summary}",
            "Security Alert: Mint authority appears enabled longer than expected. {summary}",
            "Security Alert: Liquidity path looks unusual for a new launch. {summary}",
            "Security Alert: {name} shows signs of a 12-wallet bundle. Enter with extreme caution. {summary}",
            "Warning: Creator of {name} has a high correlation with previously liquidated contracts. {summary}",
            "Risk Factor: Bonding curve for {name} ({mint}) is not tracking standard SOL growth. Potential artificial volume. {summary}",
        ]

    def generate(self, summary: str, name: str, mint: str) -> str:
        template = random.choice(self.templates)
        return template.format(summary=summary, name=name, mint=mint)
