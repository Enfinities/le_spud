import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import json
import os
from decouple import config
import interactions
import time
import Alarm_Clock_functions

Var_1=config('VAR1')
Var_2=config('VAR2')
BOT_TOKEN=Var_1 + Var_2
CHANNEL_ID = config('CHANNEL_ID')
CHANNEL_ID2 = 1213674384766799873

bot = commands.Bot(command_prefix="T ", intents=discord.Intents.all())
A_FILE = "alarm.json"
alarms = {}

@bot.command()
async def set(ctx, time, *days):
    #create new alarm
    #example use : set 23:00 Wednesday Thursday Friday Saturday
    Alarm_Clock_functions.set_alarm(ctx.author.id,time,days)
    await ctx.send("Alarm Saved!")

@bot.command()
async def check(ctx):
    user_id = ctx.author.id
    all_alarms=Alarm_Clock_functions.check_alarms(user_id)
    await ctx.send(all_alarms)


bot.run(BOT_TOKEN)