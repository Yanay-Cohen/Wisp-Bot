import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
    """Cog for moderation commands like purge."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Delete a number of messages in this channel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def purge(self, interaction: discord.Interaction, number: int):
        """
        Deletes the specified number of messages in the channel.
        """
        if number < 1:
            await interaction.response.send_message("Please specify a number greater than 0.", ephemeral=True)
            return

        deleted = await interaction.channel.purge(limit=number)
        await interaction.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True)

    @purge.error
    async def purge_error(self, interaction: discord.Interaction, error):
        """
        Handles errors for the purge command.
        """
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You do not have the required permissions to use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))