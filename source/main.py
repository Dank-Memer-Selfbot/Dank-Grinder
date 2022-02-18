"""The Main file of the Project."""

# pylint: disable=invalid-name, wrong-import-order, multiple-imports, wrong-import-position

import discord, yaml
from discord.ext import commands
from rich.console import Console
from typing import Any, Dict

# --- Constants --- #


class _grinderConfig:
    """A class that contains the configuration for the grinder."""

    def __init__(self, grinderConfig: Dict[str, Any]) -> None:
        """Initializes the grinder config."""
        self.usePercentage: int = int(grinderConfig["usePercentage"])
        self.channelId: int = int(grinderConfig["channel"])
        self.grindType = grinderConfig["type"]


class _sellConfig:
    """A class that contains the sell configuration."""

    def __init__(self, sellConfig: Dict[str, Any]) -> None:
        """Initializes the sell config."""
        self.sellItems: bool = sellConfig["sellItems"]
        self.doNotSell: str = sellConfig["type"]


class _moneyConfig:
    """A class that contains the money configuration."""

    def __init__(self, money: Dict[str, Any]) -> None:
        """Initializes the money config."""
        self.transfer: bool = money["transfer"]
        self.ownerId: int = int(money["owner"])


class _config:
    """A class that contains the configuration for the bot."""

    def __init__(
        self,
        grinderConfig: Dict[str, Any],
        sellConfig: Dict[str, Any],
        moneyConfig: Dict[str, Any],
    ) -> None:
        """Initializes the config class."""
        self.grinderConfig: _grinderConfig = _grinderConfig(grinderConfig)
        self.sellConfig: _sellConfig = _sellConfig(sellConfig)
        self.moneyConfig: _moneyConfig = _moneyConfig(moneyConfig)


console = Console()
bot = commands.Bot(command_prefix=">", self_bot=True)

with open("config.yml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
with open("source/config.yml", "r", encoding="utf-8") as file:
    innerConfig = yaml.safe_load(file)
bot.token = config["token"]["selfbotToken"]
bot.legitToken = config["token"]["botToken"]
bot.config = _config(
    innerConfig["grinderConfig"], innerConfig["sell"], innerConfig["money"]
)


if __name__ == "__main__":
    bot.run(bot.token)
