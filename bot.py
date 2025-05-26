from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import asyncio

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
DISCORD_CHANNEL_ID = 1375935338786193428  # Replace with your Discord channel ID
MINECRAFT_SERVER_ADDRESS = "88.211.231.4"   # Replace with your Minecraft server address
MINECRAFT_SERVER_PORT = 25575          # Replace with your Minecraft server port
MINECRAFT_RCON_PASSWORD = os.getenv("MINECRAFT_RCON_PASSWORD")  # Add this to your .env

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

from minecraft_bridge import MinecraftBridge
from discord_bridge import DiscordBridge

minecraft_bridge = MinecraftBridge(MINECRAFT_SERVER_ADDRESS, MINECRAFT_SERVER_PORT, MINECRAFT_RCON_PASSWORD)
discord_bridge = DiscordBridge(bot, DISCORD_CHANNEL_ID, minecraft_bridge)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Bot tree: {bot.tree}")
    await sync_commands()

async def sync_commands():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.command(name="reload", hidden=True)
@commands.is_owner()
async def reload(ctx, cog: str):
    try:
        await bot.unload_extension(f"cogs.{cog}")
        await bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Reloaded cog: {cog}")
    except Exception as e:
        await ctx.send(f"Failed to reload cog: {cog}\n{e}")

@bot.command(name="pnum")
async def player_count(ctx):
    """Shows the number of players online in the Minecraft server."""
    count = await minecraft_bridge.get_player_count()
    if count is not None:
        await ctx.send(f"There are {count} players online.")
    else:
        await ctx.send("Could not retrieve player count.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == DISCORD_CHANNEL_ID:
        await discord_bridge.handle_discord_message(message)
    await bot.process_commands(message)

async def main():
    async with bot:
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())