"""Parses Messages, responds to them and calls the appropriate events."""

# pylint: disable=invalid-name, line-too-long, wrong-import-order, wrong-import-position, multiple-imports
import sys, os
sys.path.append(os.getcwd() + "/..")
import discord, re, random
from .commandParsers import commandParsers
from typing import Union, Dict, Any
from discord.ext import commands
import yaml


NestedDictType = Dict[str, Union[None, int, str, bool, list, Dict[str, Any]]]


class _converter:
    """
    A class that converts a dictionary into a class, the dictionary keys being the class attributes.
    """

    def __init__(self, dic: NestedDictType) -> None:
        """Initialize the class with the dictionary."""
        for key, value in dic.items():
            if isinstance(value, dict):
                setattr(self, key, _converter(value))
            else:
                setattr(self, key, value)


class Parser(commands.Cog):
    """Message Parser"""

    def __init__(self, bot: commands.Bot) -> None:
        """Initializes the message parser.

        Args:
            bot (commands.Bot): The bot.
        """
        self.scout = self.get_config()
        self.bot = bot

    def get_config(self):
        # TODO: Move this to scout.py
        cur_file_dir = os.path.dirname(os.path.abspath(__file__))
        with open(cur_file_dir + r"\scout.yml", "r", encoding="utf-8") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
        return config

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Returns the type of the message."""
        if not message.author.bot:
            return
            # We only want to respond to bots
        if message.channel.id != int(self.bot.config.grinderConfig.channelId):
            return
            # We only want to respond to messages in the channel

        data: NestedDictType = {"event": False, "help": False}

        if message.reference is None:
            return
            # Only for now, commands like balance and stream don't reply
        respondedTo = message.reference.cached_message
        if respondedTo is None:
            return
            # For now, as it means the message wasn't found in the cache

        if not respondedTo.content.startswith("pls"):
            # Checking if the bot is responding to a command
            return
        # If it's a command, execute the below code
        command: str = respondedTo.content.replace("pls", "").strip()
        # Findingg the command
        data["event"] = False

        if len(message.embeds) > 0:
            embed = message.embeds[0]

            if str(embed.title).lower().endswith("command"):
                data["help"] = True
                convertedData = _converter(data)
                self.bot.dispatch("dank_help", convertedData)
                return
            # Means that the embed isn't a help embed and is the actual response

            if "beg" in command:
                data = await commandParsers.beg(embed, data)
                convertedData = _converter(data)
                self.bot.dispatch("dank_beg", convertedData)
                return

            if "hl" in command:
                # Parsing highlow command
                data = await commandParsers.highlow(embed, data, message, self.bot)
                convertedData = _converter(data)
                self.bot.dispatch("dank_highlow", convertedData)
                return

            if "pm" in command:
                # TODO: Complete and move to postmemes.py
                print("PM")
                # Parsing pm command
                description = embed.description
                # Description example
                # Pick a meme to post to the internet!
                index = random.randint(0, 4)
                await message.components[0].children[index].click()
                return

        else:
            # This is run when a message doesn't have any embeds

            # Crime
            if "crime" in command:
                # TODO: Complete and move to crime.py
                index = random.randint(0, 2)
                await message.components[0].children[index].click()
                return

            if any(x in command for x in ["scout", "search"]):
                # TODO: Complete and move to scout.py
                compo = message.components[0]
                labels = [comp.label for comp in compo.children]
                indices = []
                label = None
                for i in self.scout["SCOUT_FIND"]:
                    if i in labels:
                        indices.append(labels.index(i))
                        label = i
                        break
                if indices:
                    print(f"found {label} in {labels}")
                index = indices[0] if indices else random.randint(0, 2)
                await message.components[0].children[index].click()
                return

            # Fishing
            if "fish" in command:
                data = commandParsers.fish(data, message)
                convertedData = _converter(data)
                self.bot.dispatch("dank_fish", convertedData)
                return


def setup(bot: commands.Bot) -> None:
    """Loads the Parser cog."""
    bot.add_cog(Parser(bot))
