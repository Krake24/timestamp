#!/bin/env python3
import os
import disnake
import time
from datetime import datetime
from disnake.ext import commands
from timer import timer 

second = 1
minute = 60 * second
hour = 60 * minute
day = 24 * hour

def addDay(int):
    return int + day

def subtractDay(int):
    return int - day

def addHour(int):
    return int + hour

def subtractHour(int):
    return int - hour

def addMinute(int):
    return int + minute

def subtractMinute(int):
    return int - minute

class PrintButton(disnake.ui.Button):

    def __init__(self, label, timestamp, time_format):
        super().__init__(
            style=disnake.ButtonStyle.primary,
            label=label
        )
        self.timestamp=timestamp
        self.time_format=time_format
    
    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.send_message(f"`<t:{self.timestamp}:{self.time_format}>`", ephemeral=True)

class PrintView(disnake.ui.View):
     def __init__(self, timestamp: int):
        super().__init__()
        self.add_item(PrintButton("Time only", timestamp, "t"))
        self.add_item(PrintButton("Date and Time", timestamp, "F"))
        self.add_item(PrintButton("Countdown", timestamp, "R"))

class Print(disnake.ui.Button):
    def __init__(self):
        super().__init__(
            style=disnake.ButtonStyle.success,
            label="Continue"
        )
    
    async def callback(self, inter: disnake.MessageInteraction):
        timestamp = int(inter.message.content.replace("<t:","").replace(">",""))
        self.disabled=True
        await inter.response.send_message("Pick a time", view=PrintView(timestamp), ephemeral=True)

class TimerView(disnake.ui.View):
    def __init__(self, round_to_hour: bool = True):
        super().__init__()
        self.add_item(timer.TimeChange(addDay, "+1D", disnake.ButtonStyle.danger))
        self.add_item(timer.TimeChange(subtractDay, "-1D", disnake.ButtonStyle.danger))
        self.add_item(timer.TimeChange(addHour, "+1H", disnake.ButtonStyle.primary))
        self.add_item(timer.TimeChange(subtractHour, "-1H", disnake.ButtonStyle.primary))
        if not round_to_hour:
            self.add_item(timer.TimeChange(addMinute, "+1M", disnake.ButtonStyle.secondary))
            self.add_item(timer.TimeChange(subtractMinute, "-1M", disnake.ButtonStyle.secondary))
        self.add_item(Print())

bot = commands.InteractionBot()

@bot.slash_command()
async def timestamp(inter: disnake.AppCmdInter):
    pass

@timestamp.sub_command(description="Set timestamp based on the current time")
async def now(inter: disnake.AppCmdInter, round_to_hour: bool = True):
    t = int(time.time())
    if round_to_hour:
        t = t - (int(time.time()) % 3600) + 3600
    await inter.response.send_message(f"<t:{t}>", view=TimerView(round_to_hour), ephemeral=True)

@timestamp.sub_command(description="Set timestamp based on time from now on")
async def in_(inter: disnake.AppCmdInter, days: int = 0, hours: int = 0, minutes: int = 0, round_to_hour: bool = True):
    t = time.time()
    if round_to_hour:
        t = t - (int(time.time()) % 3600) + 3600
        minutes = 0
    t = int(t) + (days * day) + (hours * hour) + (minutes * minute)
    await inter.response.send_message(f"<t:{t}>", view=TimerView(round_to_hour), ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))