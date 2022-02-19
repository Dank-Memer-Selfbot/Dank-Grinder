import re
import discord
from discord.ext import commands
from typing import Union, Dict, Any

NestedDictType = Dict[str, Union[None, int, str, bool, list, Dict[str, Any]]]


def fish(data: NestedDictType, message: discord.Message) -> NestedDictType:
    """The fish function to parse the fish command

    Args:
        data (NestedDictType): The data to parse.
        message (discord.Message): The message to parse.

    Returns:
        NestedDictType: The parsed data.
    """
    data["event"] = False
    data["help"] = False
    data["type"] = "fish"

    gained: NestedDictType = {
        "amount": None,
        "item": None,
    }

    try:
        found = message.content.split("back")[1]
    except IndexError:
        data["gained"] = False
        return data
    # Check the amount of items gained
    gained["amount"] = re.findall("[0-9]+", found)[0]
    # Check the item(s) gained
    gained["item"] = found.strip().split()[1:-1]

    data["gained"] = gained
    return data
