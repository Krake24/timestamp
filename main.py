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

bot = commands.InteractionBot()

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

class HourMinus(disnake.ui.Button):

    def __init__(self):
        super().__init__(
            style=disnake.ButtonStyle.success,
            label="-1H"
        )
    
    async def callback(self, inter: disnake.MessageInteraction):
        timestamp = int(inter.message.content.replace("<t:","").replace(">",""))
        await inter.response.edit_message(f"<t:{timestamp - hour}>")

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

class TimerView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(timer.TimeChange(addDay, "+1D", disnake.ButtonStyle.danger))
        self.add_item(timer.TimeChange(subtractDay, "-1D", disnake.ButtonStyle.danger))
        self.add_item(timer.TimeChange(addHour, "+1H", disnake.ButtonStyle.primary))
        self.add_item(timer.TimeChange(subtractHour, "-1H", disnake.ButtonStyle.primary))
        self.add_item(Print())

@bot.slash_command()
async def timestamp(inter: disnake.AppCmdInter):
    t = int(time.time()) - (int(time.time()) % 3600) + 3600
    await inter.response.send_message(f"<t:{t}>", view=TimerView(), ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n------")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))