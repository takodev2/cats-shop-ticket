import os
import discord
from discord.ext import commands
from threading import Thread
from flask import Flask

from config import TOKEN
from cog.ticket import TicketView, TicketPanel

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
        self.add_view(TicketPanel())
        self.add_view(TicketView())
        await self.load_extension("cog.ticket")
        await self.tree.sync()

bot = MyBot()

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot.run(TOKEN)
