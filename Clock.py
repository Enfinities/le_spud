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
CHANNEL_ID2 = 1193641674237296732
CHANNEL_ID3 = 1193614896395452659
bot = commands.Bot(command_prefix="Clock ", intents=discord.Intents.all())

#C
# Function to create a JSON file for each day of the week
def create_weekly_alarm_files():
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days_of_week:
        filename = f"{day.lower()}_alarms.json"
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump({}, f)
def save_alarm(day_of_week, user_id, alarm_time):
    filename = f"{day_of_week.lower()}_alarms.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            alarms = json.load(f)
    else:
        alarms = {}

    alarms[user_id] = alarm_time

    with open(filename, "w") as f:
        json.dump(alarms, f, indent=4)

# Function to add an alarm for a specific day of the week
def add_alarm(day_of_week, user_id, alarm_time):
    filename = f"{day_of_week.lower()}_alarms.json"
    with open(filename, "r") as f:
        alarms = json.load(f)
    alarms[str(user_id)] = alarm_time
    with open(filename, "w") as f:
        json.dump(alarms, f)


# Function to save an alarm to the corresponding JSON file



# Function to check alarms every minute
def check_alarms():
    while True:
        current_day = datetime.datetime.now().strftime("%A").lower()
        filename = f"{current_day}_alarms.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                alarms = json.load(f)
            current_time = datetime.datetime.now().strftime("%H:%M")
            for user_id, alarm_time in alarms.items():
                if alarm_time == current_time:
                    print(f"Alarm for user {user_id} on {current_day} at {alarm_time}!")
        time.sleep(60)  # Check every minute

# Example usage
create_weekly_alarm_files()
add_alarm("Monday", 123456789, "08:00")
check_alarms()
#--------startup message
@bot.event
async def on_ready():
    print("Hello!Alarm bot is ready")
    channel = bot.get_channel(CHANNEL_ID2)
    await channel.send("Alarm functions ready!")

#----------------------------userside-------------------------------------
#CREATE
# Command to create an alarm entry
@bot.command()
async def create_alarm(ctx, day_of_week: str, alarm_time: str):
    day_of_week = day_of_week.capitalize()
    if day_of_week not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        await ctx.send("Invalid day of the week.")
        return

    user_id = str(ctx.author.id)
    save_alarm(day_of_week, user_id, alarm_time)
    await ctx.send(f"Alarm set for {day_of_week} at {alarm_time}.")
#READ
# Function to get a list of alarms for a specific day of the week
def get_alarms(day_of_week):
    filename = f"{day_of_week.lower()}_alarms.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            alarms = json.load(f)
        return alarms
    else:
        return {}

# Command to see a list of alarms for each day of the week
@bot.command()
async def list_alarms(ctx):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days_of_week:
        alarms = get_alarms(day)
        if alarms:
            alarm_list = "\n".join([f"{user_id}: {alarm_time}" for user_id, alarm_time in alarms.items()])
            await ctx.send(f"Alarms for {day}: \n{alarm_list}")
        else:
            await ctx.send(f"No alarms for {day}.")

#U
#D
@bot.command()
async def delete(ctx, day_of_week: str, alarm_time: str):
    # Check if the day of the week is valid
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if day_of_week.capitalize() not in valid_days:
        await ctx.send("Invalid day of the week.")
        return

    # Get the ID of the member who invoked the command
    user_id = str(ctx.author.id)

    # Delete the alarm
    if delete_alarm(day_of_week, user_id, alarm_time):
        await ctx.send(f"Alarm deleted successfully for {day_of_week} at {alarm_time}.")
    else:
        await ctx.send("No alarm found to delete for this day and time.")