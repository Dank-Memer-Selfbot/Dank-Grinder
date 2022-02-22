"""Meant for handling tasks, essentially commands that are run at specific intervals."""

import discord
from .cooldowns import Cooldowns
from discord.ext import commands, tasks


class loop(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.cooldowns = Cooldowns(bot)

    @tasks.loop(seconds=Cooldowns["beg"])
    async def beg(self) -> None:
        message = await self.bot.use_command("beg")
        data = await self.bot.wait_for("dank_beg", timeout=30)
        print(data.__dict__)

    @tasks.loop(seconds=Cooldowns["fish"])
    async def fish(self) -> None:
        message = await self.bot.use_command("fish")
        data = await self.bot.wait_for("dank_fish", timeout=30)
        print(data.__dict__)

    @tasks.loop(seconds=Cooldowns["hunt"])
    async def fish(self) -> None:
        message = await self.bot.use_command("hunt")
        data = await self.bot.wait_for("dank_hunt", timeout=30)
        print(data.__dict__)


def setup(bot: commands.Bot) -> None:
    """Meant for handling tasks, essentially commands that are run at specific intervals."""
    bot.add_cog(loop(bot))
