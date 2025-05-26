from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import asyncio

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages
intents.members = True  # Required for on_member_join and on_member_remove

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Bot tree: {bot.tree}")
    await sync_commands()

async def sync_commands():
    """
    Syncs slash commands with Discord.
    """
    try:
        # Sync new slash commands
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.command(name="reload", hidden=True)
@commands.is_owner()  # Restrict this command to the bot owner
async def reload(ctx, cog: str):
    """
    Reloads a specific cog.
    Usage: !reload <cog_name>
    """
    try:
        await bot.unload_extension(f"cogs.{cog}")
        await bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Reloaded cog: {cog}")
    except Exception as e:
        await ctx.send(f"Failed to reload cog: {cog}\n{e}")

# Dynamically load all cogs from the cogs folder
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":  # Skip __init__.py
            await bot.load_extension(f"cogs.{filename[:-3]}")

# Run the bot
async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

asyncio.run(main())