import discord
from discord.ext import commands
import json
import os

class Leveling(commands.Cog):
    """Cog for leveling system."""

    def __init__(self, bot):
        self.bot = bot
        self.levels_file = "levels.json"
        self.roles = {
            1: "Genin",
            10: "Chunnin",
            20: "Jonin",
            35: "Anbu"
        }
        # Load levels data
        if not os.path.exists(self.levels_file):
            with open(self.levels_file, "w") as f:
                json.dump({}, f)

    def load_levels(self):
        with open(self.levels_file, "r") as f:
            return json.load(f)

    def save_levels(self, data):
        with open(self.levels_file, "w") as f:
            json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore bot messages

        # Load levels data
        levels = self.load_levels()
        user_id = str(message.author.id)

        # Add XP
        if user_id not in levels:
            levels[user_id] = {"xp": 0, "level": 1}
        levels[user_id]["xp"] += 1

        # Calculate level
        new_level = levels[user_id]["xp"] // 100
        if new_level > levels[user_id]["level"]:
            levels[user_id]["level"] = new_level
            await message.channel.send(f"🎉 {message.author.mention} leveled up to **Level {new_level}**!")

            # Assign role based on level
            guild = message.guild
            for level, role_name in self.roles.items():
                role = discord.utils.get(guild.roles, name=role_name)
                if new_level >= level and role:
                    await message.author.add_roles(role)
                    await message.channel.send(f"🎉 {message.author.mention} has been promoted to **{role_name}**!")

        # Save levels data
        self.save_levels(levels)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Assign 'Genin' role to new members."""
        role = discord.utils.get(member.guild.roles, name="Genin")
        if role:
            await member.add_roles(role)
            print(f"Assigned 'Genin' role to {member.name}.")

async def setup(bot):
    await bot.add_cog(Leveling(bot))