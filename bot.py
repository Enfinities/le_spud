import datetime
from discord.ext import commands
import discord
from dataclasses import dataclass


VAR_1 = 'MTIwODI0NDI0OTk0MzA4MDk4MA.GOG7YU.PIr4Rm-'
VAR_2 = 'lfqPAHOcuhDgqLhOKyj9iroUsRuWapY'
BOT_TOKEN = VAR_1 + VAR_2
CHANNEL_ID = 1208251750524526632

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="Spud ", intents=discord.Intents.all())
session = Session()


@bot.event
async def on_ready():
    print("Hello!Le Spud is ready")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Le Spud is ready!")

#Le Spud greetings [hello,hey,hi,sup]
@bot.command()
async def hello(ctx):
    await ctx.send("Bonjour!")

@bot.command()
async def hey(ctx):
    await ctx.send("Bonjour!")

@bot.command()
async def hi(ctx):
    await ctx.send("Bonjour!")

@bot.command()
async def sup(ctx):
    await ctx.send("Sup!")

@bot.command()
async def greetings(ctx):
    await ctx.send("and Salutations to you!")

# Le Spud guide
@bot.command()
async def info(ctx):
    await ctx.send("To use Le Spud call `'Spud'` then enter a command: (**various greetings**),(**timer**:`'start'`,`'end'`)(**Maths**:`'add'` followed by numbers)(**help**:`'info'`) ")
#Le Spud Math brain
@bot.command()
async def add(ctx,*arr):
    result = 0
    for i in arr:
         result += int(i)
    await ctx.send(f"Result: {result}")

#Le Spud timer
@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    await ctx.send(f"New session started at {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is currently active!")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    await ctx.send(f"Session ended at {human_readable_time}. Duration {human_readable_duration}")



bot.run(BOT_TOKEN)