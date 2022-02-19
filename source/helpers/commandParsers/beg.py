import re, discord
from typing import Union, Dict, Any

NestedDictType = Dict[str, Union[None, int, str, bool, list, Dict[str, Any]]]


async def beg(embed: discord.Embed, data: NestedDictType) -> NestedDictType:
    """The beg function to parse the beg command.

    Args:
        embed (discord.Embed): The embed to add the beg command to.
        data (NestedDictType): The data to parse.

    Returns:
        NestedDictType: The parsed data.
    """
    data["event"] = False
    data["help"] = False
    data["type"] = "beg"
    # example description: "Oh you poor little beggar, take ⏣ 1,613 and a :dankCandy: Candy"
    # We only want the number (1613) and Union items gained
    description = str(embed.description).replace(",", "")
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
        return data
    # use the u'[a-zA-Z]+' regex to find the items gained
    items = description.split(":")[1].split(":")[1].strip().replace('"').split()[0]
    # Splits "Oh you poor little beggar, take ⏣ 1,613 and a :dankCandy: Candy" into a list
    # ["Oh you poor little beggar, take ⏣ 1,613 and a ", "dankCandy: Candy"], then splits the second element into a list
    # ["dankCandy", "Candy"], then the quotes are removed from "Candy" and so are Union other emojis.

    footer = embed.footer.text
    # Example footer: Multi Bonus: +81% (⏣ 572)
    # regex to find bonus '\+[0-9]+% \(⏣ [0-9]+\)'
    foundBonus = re.findall(r"\+[0-9]+% \(⏣ [0-9]+\)", footer)[0].split(" ")[0]
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
    return data
