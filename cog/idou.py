import discord
from discord import app_commands
from discord.ext import commands

class CategoryMove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="category-移動", description="チャンネルを指定したカテゴリーに移動します")
    @app_commands.describe(channel="移動させるチャンネル", category="移動先のカテゴリー")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def move_category(self, interaction: discord.Interaction, channel: discord.TextChannel, category: discord.CategoryChannel):
        await interaction.response.defer(ephemeral=True)
        try:
            await channel.edit(category=category)
            await interaction.followup.send(f"{channel.mention} を {category.name} に移動しました。")
        except discord.Forbidden:
            await interaction.followup.send("権限が不足しているため移動できません。")
        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました: {e}")

async def setup(bot):
    await bot.add_cog(CategoryMove(bot))
