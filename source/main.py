import discord, yaml
from discord.ext import commands
from rich.console import Console
from typing import List, Dict, Union


# --- Constants --- #


class _grinderConfig:
    """A class that contains the configuration for the grinder."""

    def __init__(self, grinderConfig: Dict[str, Union[int, str]]) -> None:
        """Initializes the grinder config."""
        self.usePercentage: int = int(grinderConfig["usePercentage"])
        self.channelId: int = int(grinderConfig["channel"])
        self.grindType: Union["levels", "money"] = grinderConfig["type"]


class _sellConfig:
    """A class that contains the sell configuration."""

    def __init__(self, sellConfig: Dict[str, Union[int, str]]) -> None:
        """Initializes the sell config."""
        self.sellItems: bool = sellConfig["sellItems"]
        self.doNotSell: List = sellConfig["type"]


class _moneyConfig:
    """A class that contains the money configuration."""

    def __init__(self, money: Dict[str, Union[str, int]]) -> None:
        """Initializes the money config."""
        self.transfer: bool = money["transfer"]
        self.ownerId: int = int(money["owner"])


class _config:
    """A class that contains the configuration for the bot."""

    def __init__(
        self,
        grinderConfig: Dict[str, Union[str, int, float]],
        sellConfig: Dict[str, Union[str, int, float]],
        moneyConfig: Dict[str, Union[str, int, float]],
    ) -> None:
        """Initializes the config class."""
        self.grinderConfig: Dict[str, Union[str, int, float]] = _grinderConfig(
            grinderConfig
        )
        self.sellConfig: Dict[str, Union[str, int, float]] = _sellConfig(sellConfig)
        self.moneyConfig: Dict[str, Union[str, int, float]] = _moneyConfig(moneyConfig)


console = Console()
bot = commands.Bot(command_prefix=">", self_bot=True)

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)
with open("./source/config.yml", "r") as file:
    innerConfig = yaml.safe_load(file)
bot.token = config["selfbotToken"]
bot.legitToken = config["botToken"]
bot.config = _config(
    innerConfig["grinderConfig"], innerConfig["sell"], innerConfig["money"]
)


if __name__ == "__main__":
    bot.run(bot.token)
