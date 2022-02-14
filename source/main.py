"""The main file, just to run the bot. This file will import extensions and tasks from other files and run them."""

# pylint: disable = wrong-import-order, multiple-imports, no-member, line-too-long

import rich, discord, yaml
from discord.ext import commands
from rich.console import Console

# --- Constants --- #

bot = commands.Bot()
bot.console = Console()
with open('config.yml', "r", encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)
bot.config = config
del config


# --- Events --- #

@bot.event
async def on_ready():
    """Runs when the bot is ready."""
    bot.console.log(f"Logged in as {bot.user} and in {len(bot.guilds)} guilds.")

# --- Commands --- #

@bot.command(help="A command to ping the bot.")
async def ping(ctx):
    """A command to ping the bot."""
    await ctx.send(f"Pong, {round(bot.latency * 1000)}ms.")

# --- Running the bot --- #

bot.run(bot.config['token'])