import random, re, discord
from discord.ext import commands
from typing import Union, Dict, Any

NestedDictType = Dict[str, Union[None, int, str, bool, list, Dict[str, Any]]]


async def highlow(
    embed: discord.Embed,
    data: NestedDictType,
    message: discord.Message,
    bot: commands.Bot,
) -> NestedDictType:
    """The highlow function to parse the highlow command.

    Args:
        embed (discord.Embed): The embed to add the highlow command to.
        data (NestedDictType): The data to parse.
        message (discord.Message): The message to parse.
        bot (commands.Bot): The bot.

    Returns:
        NestedDictType: The parsed data.
    """
    data["type"] = "dank_highlow"
    description = embed.description
    # Description example:
    # I just chose a secret number between 1 and 100.
    # Is the secret number higher or lower than 50.
    footer = embed.footer.text
    # Example: The jackpot button is if you think it's the same!
    numberLine = description.split("\n")[1]
    number = int(re.findall(r"\*\*[0-9]+\*\*", numberLine)[0].replace("**", ""))
    components = message.components
    low, high = components[0].children[0], components[0].children[2]
    # This is a game of highlow, we are given a hint between 1 and 100 and we need to guess if the secret number is greater than, smaller than, or is the hint
    if number == 50:
        await components[0].children[random.randint(0, 2)].click
    elif number > 50:
        await low.click()
    else:
        await high.click()

    oldMessage, newMessage = await bot.wait_for(
        "message_edit",
        check=lambda oldMsg, newMsg: oldMsg.id == message.id,
        timeout=None,
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
    return data
