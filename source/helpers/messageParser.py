"""Parses Messages, responds to them and calls the appropriate events."""

# pylint: disable=invalid-name, line-too-long, wrong-import-order, wrong-import-position, multiple-imports

import sys, os

sys.path.append(os.getcwd() + "/..")
import discord, re, random
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
        self.bot: commands.Bot = bot

    def get_config(self):
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
        if message.channel.id != self.bot.config.channelId:
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
        if message.content.embeds:
            embed = message.content.embeds[0]
            if embed.title.lower().endswith("command"):
                data["help"] = True
                convertedData = _converter(data)
                self.bot.dispatch("dank_help", convertedData)
                return
            # Means that the embed isn't a help embed and is the actual response

            if "beg" in command:
                data["event"] = True
                data["help"] = False
                data["type"] = "beg"
                # example description: "Oh you poor little beggar, take ⏣ 1,613 and a :dankCandy: Candy"
                # We only want the number (1613) and Union items gained
                description = embed.description.replace(",", "")
                gained: NestedDictType = {
                    "money": None,
                    "items": None,
                    "bonus": None,
                }
                # use the u'⏣ [0-9]+' regex to find the money gained
                try:
                    money = re.findall("⏣ [0-9]+", description)[0].split(" ")[1]
                except IndexError:
                    # Only called when the regex doesn't find Unionthing, which it can't in cases like
                    # "HeRe In AmErIcA wE dOnT dO cOmMuNiSm"
                    # Which mains no money was gained
                    data["gained"] = False
                    convertedData = _converter(data)
                    self.bot.dispatch("dank_beg", convertedData)
                    del convertedData
                    return
                # use the u'[a-zA-Z]+' regex to find the items gained
                items = (
                    description.split(":")[1]
                    .split(":")[1]
                    .strip()
                    .replace('"')
                    .split()[0]
                )
                # Splits "Oh you poor little beggar, take ⏣ 1,613 and a :dankCandy: Candy" into a list
                # ["Oh you poor little beggar, take ⏣ 1,613 and a ", "dankCandy: Candy"], then splits the second element into a list
                # ["dankCandy", "Candy"], then the quotes are removed from "Candy" and so are Union other emojis.

                footer = embed.footer.text
                # Example footer: Multi Bonus: +81% (⏣ 572)
                # regex to find bonus '\+[0-9]+% \(⏣ [0-9]+\)'
                foundBonus = re.findall(r"\+[0-9]+% \(⏣ [0-9]+\)", footer)[0].split(
                    " "
                )[0]
                bonus: NestedDictType = {
                    "percent": None,
                    "money": None,
                }
                foundBonus = (
                    foundBonus.replace("+", "")
                    .replace("%", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace("⏣", "")
                )
                foundBonus = foundBonus.split(" ")
                bonus["percent"] = int(foundBonus[0])
                bonus["money"] = int(foundBonus[1])
                gained["bonus"] = bonus
                gained["money"] = int(money)
                gained["items"] = items
                data["gained"] = gained
                convertedData = _converter(data)
                self.bot.dispatch("dank_beg", convertedData)

            if "hl" in command:
                # Parsing highlow command
                data["type"] = "dank_highlow"
                description = embed.description
                # Description example:
                # I just chose a secret number between 1 and 100.
                # Is the secret number higher or lower than 50.
                footer = embed.footer.text
                # Example: The jackpot button is if you think it's the same!
                numberLine = description.split("\n")[1]
                number = int(
                    re.findall(r"\*\*[0-9]+\*\*", numberLine)[0].replace("**", "")
                )
                components = message.components
                low = components[0].children[0]
                high = components[0].children[2]
                # This is a game of highlow, we are given a hint between 1 and 100 and we need to guess if the secret number is greater than, smaller than, or is the hint
                if number == 50:
                    # If the number is 50, we can pick a random choice between above and below
                    if random.randint(0, 1) == 0:
                        await low.click()
                    else:
                        await high.click()
                elif number > 50:
                    await low.click()
                else:
                    await high.click()
                oldMessage, newMessage = await self.bot.wait_for(
                    "message_edit", check=lambda m: m.author == message.author
                )
                del oldMessage
                embed = newMessage.embeds[0]
                footer = embed.footer.text
                description = embed.description
                # Gets the embed footer, the footer is loser loser if you lose, the color of the embed can also be checked
                if "loser" in footer:
                    data["lost"] = True
                    data["amount"] = None
                # example desc when you win
                # **You won ⏣ 2,197!**
                # \n
                # Your hint was **49**. The hidden number was **94**.
                if "won" in description:
                    data["won"] = True
                    data["amount"] = int(
                        re.findall(r"⏣ [0-9]+", description)[0].replace("⏣", "").strip()
                    )
                convertedData = _converter(data)
                self.bot.dispatch("dank_highlow", convertedData)

            if "pm" in command:
                print("PM")
                # Parsing pm command
                description = embed.description
                # Description example
                # Pick a meme to post to the internet!
                index = random.randint(0, 4)
                try:
                    await message.components[0].children[index].click()
                except discord.errors.DiscordServerError:
                    await message.components[0].children[index].click()
                return

        else:
            # This is run when a message doesn't have any embeds

            # Crime
            if "crime" in command:
                index = random.randint(0, 2)
                try:
                    await message.components[0].children[index].click()
                except discord.errors.DiscordServerError:
                    await message.components[0].children[index].click()
                return

            if any(x in command for x in ["scout", "search"]):
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

                try:
                    await message.components[0].children[index].click()
                except discord.errors.DiscordServerError:
                    await message.components[0].children[index].click()


def setup(bot: commands.Bot) -> None:
    """Loads the Parser cog."""
    bot.add_cog(Parser(bot))
