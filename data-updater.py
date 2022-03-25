import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
fulldata = dict

bot = commands.Bot(command_prefix="api!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("connected")


@bot.command()
@commands.has_permissions(administrator=True)
async def forceupdate(ctx):
    loaddata()
    membercount = 0
    for member in ctx.guild.members:
        membercount += 1
        
    rolecount = 0
    for role in ctx.guild.roles:
        rolecount += 1
    
    channelcount = 0
    for channel in ctx.guild.channels:
        channelcount += 1
        
    twilightcount = 0
    for twilight in ctx.guild.get_role(891662079336005642).members:
        twilightcount += 1
        
    boostcount = ctx.guild.premium_subscription_count

    fulldata["Serverstats"]["membercount"] = membercount
    fulldata["Serverstats"]["rolecount"] = rolecount
    fulldata["Serverstats"]["boosts"] = boostcount
    fulldata["Serverstats"]["twilights"] = twilightcount
    fulldata["Serverstats"]["channel"] = channelcount
    savedata()

    url = bot.get_user(355004590602846208).avatar.url
    embed = discord.Embed(
        title="Twilight Dawn Developer API",
        description="Updated local serverinfo api data.\n"
                    "\n"
                    "Available on: `https://176f-116-202-42-57.ngrok.io/api/v1/serverinfo`"
    )
    embed.set_footer(icon_url=url, text="Developed by kiisuhh#2750")

    await ctx.reply(embed=embed)


def loaddata():
    global fulldata
    with open("data.json", "r") as f:
        fulldata = json.load(f)


def savedata():
    global fulldata
    with open("data.json", "w") as f:
        json.dump(fulldata, f, indent=4)


bot.run(os.getenv("TOKEN"))
