import discord
from typing import Union, Dict, Any

NestedDictType = Dict[str, Union[None, int, str, bool, list, Dict[str, Any]]]


def hunt(data: NestedDictType, message: discord.Message) -> NestedDictType:

    """The hunt function to parse the hunt command

    Args:
        data (NestedDictType): The data to parse.
        message (discord.Message): The message to parse.

    Returns:
        NestedDictType: The parsed data.
    """
    data["event"] = False
    data["help"] = False
    data["type"] = "hunt"

    gained: NestedDictType = {
        "item": None,
    }
    try:
        found = message.content.split("back")[1]
    except IndexError:
        data["gained"] = False
        return data

    gained["item"] = found.split()[1]
    data["gained"] = gained
    return data
