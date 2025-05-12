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
        # Debugging: Print when the event is triggered
        print(f"on_member_join triggered for {member.name}")

        # Replace 'YOUR_CHANNEL_ID' with the ID of your welcome channel
        channel = member.guild.get_channel(1369400705235947602)
        print(f"Channel found: {channel}")  # Debugging: Check if the channel is found

        if channel:
            await channel.send(f"Welcome to wisp!, {member.mention}! 🎉")
        else:
            print("Welcome channel not found.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        Event listener that triggers when a member leaves the server.
        """
        # Debugging: Print when the event is triggered
        print(f"on_member_remove triggered for {member.name}")

        # Replace 'YOUR_CHANNEL_ID' with the ID of your welcome channel
        channel = member.guild.get_channel(1369400705235947602)
        print(f"Channel found: {channel}")  # Debugging: Check if the channel is found

        if channel:
            await channel.send(f"Goodbye, {member.name}. Dont join maid cafe! 😢")
        else:
            print("Welcome channel not found.")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(Welcome(bot))