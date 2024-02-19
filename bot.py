import datetime
from discord.ext import commands
import discord
from dataclasses import dataclass
import json
import os

VAR_1 = 'MTIwODI0NDI0OTk0MzA4MDk4MA.GOG7YU.PIr4Rm-'
VAR_2 = 'lfqPAHOcuhDgqLhOKyj9iroUsRuWapY'
BOT_TOKEN = VAR_1 + VAR_2
CHANNEL_ID = 1208251750524526632
CHANNEL_ID2 = 1193614896395452659
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

#Le spud quotes

# Define the path to the JSON file where quotes will be stored
QUOTES_FILE = 'quotes.json'




@bot.command()
async def quote(ctx, *, quote):
    """
    Command to add a quote to the JSON file.
    Usage: quote me [quote]
    """
    with open(QUOTES_FILE, 'r+') as f:
        quotes = json.load(f)
        quotes.append(quote)
        f.seek(0)
        json.dump(quotes, f, indent=4)
    await ctx.send('Quote added successfully!')

@bot.command()
async def quotes(ctx):
    """
    Command to list all quotes stored in the JSON file.
    Usage: quote list
    """
    with open(QUOTES_FILE, 'r') as f:
        quotes = json.load(f)
    if quotes:
        quotes_list = '\n'.join(quotes)
        await ctx.send(f'**Quotes:**\n{quotes_list}')
    else:
        await ctx.send('No quotes found.')

# Ensure the JSON file exists and contains an empty list if it doesn't exist yet
try:
    with open(QUOTES_FILE, 'r') as f:
        pass
except FileNotFoundError:
    with open(QUOTES_FILE, 'w') as f:
        json.dump([], f)

if __name__ == "__main__":
    # Set the cwd to the directory where this file lives
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

bot.run(BOT_TOKEN)