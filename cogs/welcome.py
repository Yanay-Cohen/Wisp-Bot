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
        # Use the channel ID directly
        channel = member.guild.get_channel(1369400705235947602)

        if channel:
            # Create an embed for the welcome message
            embed = discord.Embed(
                title="🎉 Welcome to Wisp! 🎉",
                description=(
                    f"Welcome to the server, {member.mention}!\n\n"
                    "We're thrilled to have you here. Go get some grips!, "
                ),
                color=discord.Color.blue()
            )
            embed.set_image(url="https://i.ibb.co/hR4TW388/welcome-image.png")
            embed.set_footer(text="Enjoy your stay! 🌟")

            # Send the embed to the welcome channel
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        Event listener that triggers when a member leaves the server.
        """
        # Use the channel ID directly
        channel = member.guild.get_channel(1369400705235947602)

        if channel:
            await channel.send(f"Goodbye, {member.name}. Don't join maid cafe! 😢")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(Welcome(bot))