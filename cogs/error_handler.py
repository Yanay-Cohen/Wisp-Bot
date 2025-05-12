import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    """Cog for handling errors globally."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Handles errors for all commands globally.
        """
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions to use this command.", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You are missing a required argument. Please check the command usage.", delete_after=5)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("That command does not exist. Please check the available commands.", delete_after=5)
        else:
            print(f"Unhandled error: {error}")
            await ctx.send("An unexpected error occurred. Please contact the bot administrator.", delete_after=5)

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))