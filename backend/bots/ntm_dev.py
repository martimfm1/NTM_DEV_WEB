import discord
from discord.ext import commands, tasks
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = True
intents.presences = True
intents.reactions = True
intents.integrations = True

bot = commands.Bot(command_prefix='0001', intents=intents)
@bot.event
async def on_ready():
    print(f"✅ {bot.user} Ligou!")
