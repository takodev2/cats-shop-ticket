import os
import discord
from discord.ext import commands
from threading import Thread
from flask import Flask

from config import TOKEN
from cog.vend import VendView

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive"

def run_web():
    app.run(host='0.0.0.0', port=8080)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):

        self.add_view(VendView()

        await self.load_extension("cog.vend"))
        await self.tree.sync()

bot = MyBot()

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot.run(TOKEN)
