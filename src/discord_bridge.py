import discord

class DiscordBridge:
    def __init__(self, bot, channel_id, minecraft_bridge):
        self.bot = bot
        self.channel_id = channel_id
        self.minecraft_bridge = minecraft_bridge

    async def send_to_discord(self, player, message):
        """Send a message from Minecraft to the Discord channel."""
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send(f"**{player}**: {message}")

    async def handle_discord_message(self, message):
        """Relay a Discord message to Minecraft chat."""
        if message.author.bot:
            return
        if message.channel.id != self.channel_id:
            return
        # Format: [Discord] Username: message
        mc_message = f"[Discord] {message.author.display_name}: {message.content}"
        await self.minecraft_bridge.send_message(mc_message)