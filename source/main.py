"""The Main file of the Project."""

# pylint: disable=invalid-name, wrong-import-order, multiple-imports, wrong-import-position
import os
import discord, yaml
from discord.ext import commands
from rich.console import Console
from typing import Any, Dict
from helpers.messageParser import *
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
        self.doNotSell: str = sellConfig["doNotSell"]


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


#console = Console()
bot = commands.Bot(command_prefix='', self_bot=True)

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')
    
@bot.event
async def on_message(message):
    # Base Cases
    if message.author == bot.user:
        return
    
cur_file_dir = os.path.dirname(os.path.abspath(__file__))
with open(cur_file_dir+"/config.yml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
bot.token = config["token"]["selfbotToken"]
bot.legitToken = config["token"]["botToken"]
bot.config = _config(
    config["grinderConfig"], config["sell"], config["money"]
)

async def use_command(command: str) -> bool:
    """Uses a command

    Args:
        command (str): The command to use.

    Returns:
        bool: Whether the command was used.
    """
    channel = bot.get_channel(bot.config.grinderConfig.channelId)
    if channel is None:
        channel = await bot.fetch_channel(bot.config.grinderConfig.channelId)
    if channel is None:
        raise Exception("Channel not found")
    await channel.send(command)
    return True

bot.use_command = use_command
# This allows for easy changeability, especially with dank memer's update coming soon


if __name__ == "__main__":
    bot.add_cog(Parser(bot))
    bot.run(bot.token)
