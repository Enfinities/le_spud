import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import json
import os
from decouple import config
import interactions
import time
Var_1=config('VAR1')
Var_2=config('VAR2')
BOT_TOKEN=Var_1 + Var_2
CHANNEL_ID = config('CHANNEL_ID')
CHANNEL_ID2 = 1213674384766799873

bot = commands.Bot(command_prefix="T ", intents=discord.Intents.all())
A_FILE = "alarm.json"
#-----------------Create
def set_alarm(user_id, time, days):
    # Load existing alarms or create a new dictionary
    try:
        with open(A_FILE, "r") as f:
            alarms = json.load(f)
    except FileNotFoundError:
        alarms = {}

    # Update alarms dictionary with new alarm data
    alarms[user_id] = [{
        "time": time,
        "days_of_week": {day: (day in days) for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
    }]

    # Write updated alarms dictionary to JSON file
    with open(A_FILE, "w") as f:
        json.dump(alarms, f, indent=4)

#------------------Read
def check_alarms(user_id):
    try:
        with open(A_FILE, "r") as f:
            alarms = json.load(f)
    except FileNotFoundError:
        alarms = {}

    user_alarms = alarms.get(str(user_id), {})

    if user_alarms:
        return user_alarms
    else:
        return "You have no alarms set."
#-------------------update
#-------------------Delete
def delete_alarm(user_id, alarm_time):
    try:
        with open("alarms.json", "r") as f:
            alarms = json.load(f)
    except FileNotFoundError:
        alarms = {}

    if str(user_id) in alarms:
        user_alarms = alarms[str(user_id)]
        if alarm_time in user_alarms:
            del user_alarms[alarm_time]
            with open("alarms.json", "w") as f:
                json.dump(alarms, f, indent=4)
            return f"Alarm at {alarm_time} deleted successfully."
        else:
            return f"No alarm found at {alarm_time} for the specified user ID."
    else:
        return "No alarm found for the specified user ID."


#-----------------main block
if __name__ == "__main__":
    user_id = 583730259409633310
    alarms = check_alarms(user_id)
    print(alarms)