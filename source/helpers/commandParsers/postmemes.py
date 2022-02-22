import re, discord, random, asyncio
from discord.ext import commands
from typing import Union, Dict, Any

NestedDictType = Dict[str, Union[None, int, str, bool, list, Dict[str, Any]]]


async def wait_for_msg(bot: commands.Bot, msg_id: int) -> discord.Message:

    oldMessage, newMessage = await bot.wait_for(
        "message_edit",
        check=lambda oldMsg, newMsg: oldMsg.id == msg_id,
        timeout=10.0,
    )
    return newMessage


async def postmeme(
    embed: discord.Embed,
    data: NestedDictType,
    msg: discord.Message,
    bot: commands.Bot,
) -> NestedDictType:
    """The beg function to parse the beg command.

    Args:
        embed (discord.Embed): The embed to add the highlow command to.
        data (NestedDictType): The data to parse.
        msg (discord.Message): The message to parse.
        bot (commands.Bot): The bot.

    Returns:
        NestedDictType: The parsed data.


    First message
        Description : Pick a meme to post to the internet!

    Second message
        Winning
            Description : You posted a decent meme!
            Footer      : You earned **⏣ 1,752** for your funny efforts.

        Losing 1
            Description : Your meme is a DEAD BORING TERRIBLE DISGUSTING meme.
            Footer      : You get **⏣ 0** AND now your <:laptop:830509316674813974> **Laptop** is broken lmao, you have bad luck

        Losing 2
            Description :
            Footer      :
    """
    print("pm")
    # description = embed.description
    component = msg.components[0]

    index = random.randint(0, 4)
    await component.children[index].click()
    msg_id = msg.id

    # Error check to see if msg was successful
    # If Unsuccessful, return empty data
    try:
        new_message = await wait_for_msg(bot, msg_id)
    except asyncio.TimeoutError:
        return data

    embed = new_message.embeds[0]
    description = embed.description
    footer = embed.footer

    if "posted" in str(description):
        data["won"] = True
        data["amount"] = int(
            re.findall(r"⏣ [0-9]+", description)[0].replace("⏣", "").strip()
        )
        print(data["amount"])
    else:
        data["lost"] = True
        data["amount"] = None
        if "laptop" in str(footer).lower():
            data["item"] = "laptop"
    return data
