import discord
from discord.ext import commands

class Fun(commands.Cog):
    """Cog for fun commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        """Sends a hello message."""
        await ctx.send("Hello! This is a fun command.")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(Fun(bot))