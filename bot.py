import datetime
from discord.ext import commands
import discord
from dataclasses import dataclass
import json
import os
from decouple import config
import interactions
Var_1=config('VAR1')
Var_2=config('VAR2')
BOT_TOKEN=Var_1 + Var_2
#BOT_TOKEN = config('BOT_TOKEN1')
CHANNEL_ID = config('CHANNEL_ID')
CHANNEL_ID2 = 1193641674237296732
@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="Spud ", intents=discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Hello!Le Spud is ready")
    channel = bot.get_channel(CHANNEL_ID2)
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
async def yes(ctx, x, y):
    results = int(x) + int(y)
    await ctx.send(f"Sure! {x} plus {y} equals {results}")
@bot.command()
async def add(ctx, *arr):
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

#Le spud points system
POINTS_FILE = 'points.json'

def load_points():
    if not os.path.exists(POINTS_FILE):
        return {}

    with open(POINTS_FILE, 'r') as f:
        return json.load(f)
def save_points(points):
    with open(POINTS_FILE, 'w') as f:
        json.dump(points, f)

def modify_points(member_id, points_delta):
    points = load_points()
    member_id = str(member_id)
    points[member_id] = points.get(member_id, 0) + points_delta
    save_points(points)
def get_points(member_id):
    points = load_points()
    print(points)
    print(member_id)
    member_id = str(member_id)
    return points.get(member_id, 0)

#commands (plus, minus, points)
@bot.command()
async def plus(ctx, member: discord.Member, points: int):
    modify_points(member.id, points)
    await ctx.send(f"Added {points} points to {member.display_name}!")

     # Bot command to subtract points from a member
@bot.command()
async def minus(ctx, member: discord.Member, points: int):
    modify_points(member.id, -points)
    await ctx.send(f"Subtracted {points} points from {member.display_name}!")
@bot.command()
async def points(ctx, member: discord.Member = None):
    member = member or ctx.author  # Use the command invoker if member is not provided
    points = get_points(member.id)
    await ctx.send(f"{member.display_name} has {points} points!")
    #print(points)
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

#make Le bot @ppl
@bot.command()
async def target(ctx, member: discord.Member):
    await ctx.send(f"Hey {member.mention}, {ctx.author.mention} targets you")

@bot.command()
async def say(ctx, *, message: str):
    await ctx.send(message)

@bot.command()
async def tell(ctx, member: discord.Member, *, message: str):
    await ctx.send(f"Hey {member.mention}, {ctx.author.mention} has a message for you: {message}")


if __name__ == "__main__":
    # Set the cwd to the directory where this file lives
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    #Ensure the JSON file exists and contains an empty list if it doesn't exist yet
    try:
        with open(QUOTES_FILE, 'r') as f:
            pass
    except (FileNotFoundError, PermissionError):
        with open(QUOTES_FILE, 'w') as f:
            json.dump([], f)

    bot.run(BOT_TOKEN)