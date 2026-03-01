import discord
from discord.ext import commands
from discord import app_commands
import datetime
from config import LOG_CH_ID

def load_items():
    items = {}
    try:
        with open("lol.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    name, content = line.strip().split("=", 1)
                    items[name] = content
    except FileNotFoundError:
        pass
    return items

class ConfirmView(discord.ui.View):
    def __init__(self, item_name, content):
        super().__init__(timeout=None)
        self.item_name = item_name
        self.content = content

    @discord.ui.button(label="購入確定", style=discord.ButtonStyle.green, custom_id="confirm_purchase")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        now = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
        
        log_embed = discord.Embed(title="購入ログ", color=discord.Color.blue())
        log_embed.add_field(name="商品名", value=f"```{self.item_name}```", inline=False)
        log_embed.add_field(name="値段", value="```0円```", inline=False)
        log_embed.add_field(name="購入者", value=f"**{interaction.user.mention}({interaction.user.id})**", inline=False)
        
        log_ch = interaction.client.get_channel(LOG_CH_ID)
        if log_ch:
            await log_ch.send(embed=log_embed)

        dm_msg = (
            f"購入が完了しました\n購入日\n{now}\n"
            f"商品名\n{self.item_name}\n購入数\n1個\n支払金額\n0円\n\n"
            f"【内容】\n{self.content}"
        )
        
        try:
            await interaction.user.send(dm_msg)
            await interaction.response.send_message("DMに商品を送信しました。", ephemeral=True)
        except:
            await interaction.response.send_message("DM送信に失敗しました。設定を確認してください。", ephemeral=True)

class ItemSelect(discord.ui.Select):
    def __init__(self, items):
        options = [
            discord.SelectOption(label=name, description="価格: 0円｜在庫数: ∞個")
            for name in items.keys()
        ]
        super().__init__(placeholder="商品を選択してください", options=options, custom_id="item_select_menu")
        self.items = items

    async def callback(self, interaction: discord.Interaction):
        item_name = self.values[0]
        content = self.items.get(item_name, "データなし")
        
        embed = discord.Embed(title="購入確認", color=discord.Color.yellow())
        embed.add_field(name="商品名", value=f"***{item_name}***", inline=False)
        embed.add_field(name="個数", value="```1個```", inline=False)
        embed.add_field(name="金額", value="```0円```", inline=False)
        
        await interaction.response.send_message(embed=embed, view=ConfirmView(item_name, content), ephemeral=True)

class VendView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💫￤購入", style=discord.ButtonStyle.gray, custom_id="vend_buy_button")
    async def buy(self, interaction: discord.Interaction, button: discord.ui.Button):
        items = load_items()
        embed = discord.Embed(title="無料自販機", description="下記のメニューから選んで購入してください。", color=discord.Color.blue())
        view = discord.ui.View()
        view.add_item(ItemSelect(items))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class Vend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="panel", description="自販機パネルを設置します")
    async def panel(self, interaction: discord.Interaction):
        items = load_items()
        if not items:
            return await interaction.response.send_message("商品データが見つかりません。", ephemeral=True)

        desc = ""
        for name in items.keys():
            desc += f"**{name}**\n----------------\n"
        
        embed = discord.Embed(title="__無料自販機__", description=desc.strip(), color=discord.Color.green())
        await interaction.channel.send(embed=embed, view=VendView())
        await interaction.response.send_message("[+] 設置完了", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Vend(bot))
