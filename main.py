#!/bin/env python3
import os
import disnake
import time
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


class Print(disnake.ui.Button):

    def __init__(self):
        super().__init__(
            style=disnake.ButtonStyle.success,
            label="Print"
        )
    
    async def callback(self, inter: disnake.MessageInteraction):
        message=""
        timestamp = int(inter.message.content.replace("<t:","").replace(">",""))
        formats="tTdDfFR"
        for format in formats:
            message += f"`<t:{timestamp}:{format}>` => <t:{timestamp}:{format}>\n" 

        await inter.response.send_message(message, ephemeral=True)

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