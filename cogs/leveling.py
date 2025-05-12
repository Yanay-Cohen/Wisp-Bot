import discord
from discord.ext import commands
from discord import app_commands
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

            # Create a themed embed for level-up
            embed = discord.Embed(
                title="🎉 Level Up! 🎉",
                description=f"{message.author.mention}, you leveled up to **Level {new_level}**!",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Keep chatting to level up further!")
            await message.channel.send(embed=embed)

            # Assign role based on level
            guild = message.guild
            for level, role_name in self.roles.items():
                role = discord.utils.get(guild.roles, name=role_name)
                if new_level >= level and role:
                    await message.author.add_roles(role)

                    # Create a themed embed for role promotion
                    embed = discord.Embed(
                        title="🎖️ Role Promotion! 🎖️",
                        description=f"{message.author.mention} has been promoted to **{role_name}**!",
                        color=discord.Color.gold()
                    )
                    embed.set_footer(text="Congratulations on your achievement!")
                    await message.channel.send(embed=embed)

        # Save levels data
        self.save_levels(levels)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Assign 'Genin' role to new members."""
        role = discord.utils.get(member.guild.roles, name="Genin")
        if role:
            await member.add_roles(role)
            print(f"Assigned 'Genin' role to {member.name}.")

    @app_commands.command(name="setlevel", description="Set a user's level (Admin only).")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_level(self, interaction: discord.Interaction, member: discord.Member, level: int):
        """
        Slash command to set a user's level. Only administrators can use this.
        """
        if level < 1:
            embed = discord.Embed(
                title="⚠️ Invalid Level",
                description="Level must be 1 or higher.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Load levels data
        levels = self.load_levels()
        user_id = str(member.id)

        # Update level and XP
        levels[user_id] = {
            "xp": level * 100,  # Set XP based on level
            "level": level
        }

        # Assign roles based on the new level
        guild = interaction.guild
        for lvl, role_name in self.roles.items():
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                if level >= lvl:
                    await member.add_roles(role)
                else:
                    await member.remove_roles(role)

        # Save levels data
        self.save_levels(levels)

        # Create a themed embed for the response
        embed = discord.Embed(
            title="✅ Level Set Successfully",
            description=f"{member.mention}'s level has been set to **Level {level}**.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Use /setlevel to adjust levels as needed.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Leveling(bot))