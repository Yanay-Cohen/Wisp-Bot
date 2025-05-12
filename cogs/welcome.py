import discord
from discord.ext import commands

class Welcome(commands.Cog):
    """Cog for welcoming new members."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Event listener that triggers when a new member joins the server.
        """
        # Replace 'welcome-channel' with the name of your welcome channel
        channel = discord.utils.get(member.guild.text_channels, name="👋・welcome")
        if channel:
            await channel.send(f"Welcome to wisp!, {member.mention}! 🎉")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        Event listener that triggers when a member leaves the server.
        """
        # Replace 'welcome-channel' with the name of your welcome channel
        channel = discord.utils.get(member.guild.text_channels, name="👋・welcome")
        if channel:
            await channel.send(f"Goodbye, {member.name}. Dont join maid cafe! 😢")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(Welcome(bot))