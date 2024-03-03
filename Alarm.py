import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import json
import os
from decouple import config
import interactions
import time
#--------------------------backend Code----------------------------
Var_1=config('VAR1')
Var_2=config('VAR2')
BOT_TOKEN=Var_1 + Var_2
CHANNEL_ID = config('CHANNEL_ID')
CHANNEL_ID2 = 1193614896395452659

bot = commands.Bot(command_prefix="Clock ", intents=discord.Intents.all())

#--------startup message
@bot.event
async def on_ready():
    print("Hello!Alarm bot is ready")
    channel = bot.get_channel(CHANNEL_ID2)
    await channel.send("Alarm functions ready!")
    check_alarm.start()  # Start the background task

#check time each second and compare to alarm from gpt
@tasks.loop(seconds=60.0)
async def check_alarm():
    # Load alarms from JSON file
    try:
        with open("alarms.json", "r") as f:
            alarms = json.load(f)
    except FileNotFoundError:
        alarms = {}

    # Get current time and day
    current_time = datetime.datetime.now().strftime("%H:%M")
    current_day = datetime.datetime.now().strftime("%A")

    # Check for alarms
    for user_id, alarm_data in alarms.items():
        alarm_time = alarm_data["time"]
        alarm_day = alarm_data["day_of_week"]

        # Check if alarm matches current time and day
        if alarm_time == current_time and alarm_day == current_day:
            # Get member object
            member = bot.get_user(int(user_id))
            if member:
                # Mention user
                await bot.get_channel(CHANNEL_ID2).send(f"{member.mention}, it's time for your alarm!")

            else:
                print(f"User with ID {user_id} not found.")
#--------Day of week
def get_day():
    current_date = datetime.datetime.now()
    # Get the day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
    day_of_week = current_date.weekday()
    day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return day_name[day_of_week]
print("Today is", get_day())
# Date/time
def get_date():
    current_date = datetime.datetime.now().strftime("%H:%M")
    return current_date
# Example usage
print("Today is", get_date())


#------------------interface code-------------------
@bot.command()
async def date(ctx):
    await ctx.send(f"Today is {get_day()}, {get_date()}")

@bot.command()
async def set(ctx, alarm_time: str,day_of_week: str):
    # Get the ID of the member who invoked the command
    member_id = ctx.author.id

    # Check if the day of the week is valid
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if day_of_week.capitalize() not in valid_days:
        await ctx.send("Invalid day of the week.")
        return

    try:
        with open("alarms.json", "r") as f:
            alarms = json.load(f)
    except FileNotFoundError:
        alarms = {}

    alarms[str(member_id)] = {
        "time": alarm_time,
        "day_of_week": day_of_week.capitalize()
    }

    with open("alarms.json", "w") as f:
        json.dump(alarms, f, indent=4)

    await ctx.send("Alarm created successfully.")

@bot.command()
async def unset(ctx, alarm_time: str, day_of_week: str):
        try:
            with open("alarms.json", "r") as f:
                alarms = json.load(f)
        except FileNotFoundError:
            alarms = {}

        # Iterate over the alarms and remove the matching one
        for user_id, alarm_data in list(alarms.items()):
            if alarm_data["time"] == alarm_time and alarm_data["day_of_week"].capitalize() == day_of_week.capitalize():
                del alarms[user_id]

        # Write the updated alarms back to the JSON file
        with open("alarms.json", "w") as f:
            json.dump(alarms, f, indent=4)

        await ctx.send("Alarm deleted successfully.")
@bot.command()
async def alarms(ctx):
    try:
        with open("alarms.json", "r") as json_file:
            user_alarms = json.load(json_file)
    except FileNotFoundError:
        await ctx.send("No alarms found.")
        return

    # Get the ID of the member who invoked the command
    member_id = str(ctx.author.id)

    if member_id in user_alarms:
        alarm_time = user_alarms[member_id]["time"]
        alarm_day = user_alarms[member_id]["day_of_week"]
        await ctx.send(f"Your alarm is set for {alarm_time} on {alarm_day}.")
    else:
        await ctx.send("You have no alarms set.")
@bot.command()
async def info(ctx):
    await ctx.send("Thank you for using `Clock bot`! (name wip)\n"
               "To call Clock bot say '**Clock**' then say one of the following commands:\n"
               "**set**<time24h><day>, **unset**<time24h><day>**, alarms, date**")
bot.run(BOT_TOKEN)
