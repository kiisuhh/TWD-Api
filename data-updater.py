import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import datetime

load_dotenv()
fulldata = dict

bot = commands.Bot(command_prefix="api!", intents=discord.Intents.all())

async def refreshdata():

    loaddata()

    guild = bot.get_guild(871493013334007928)

    membercount = 0
    for member in guild.members:
        membercount += 1

    rolecount = 0
    for role in guild.roles:
        rolecount += 1

    channelcount = 0
    for channel in guild.channels:
        channelcount += 1

    twilightcount = 0
    for twilight in guild.get_role(891662079336005642).members:
        twilightcount += 1

    boostcount = guild.premium_subscription_count

    bancount = 0
    for bans in await guild.bans():
        bancount += 1

    ageindays = (datetime.datetime.now().date() - guild.created_at.date()).days

    bots = 0
    for member in guild.get_role(872089246729666560).members:
        bots += 1

    fulldata["Serverstats"]["membercount"] = membercount
    fulldata["Serverstats"]["rolecount"] = rolecount
    fulldata["Serverstats"]["boosts"] = boostcount
    fulldata["Serverstats"]["twilights"] = twilightcount
    fulldata["Serverstats"]["channel"] = channelcount
    fulldata["Serverstats"]["bans"] = bancount
    fulldata["Serverstats"]["days"] = ageindays
    fulldata["Serverstats"]["bots"] = bots

    #print("data updated at " + str(datetime.datetime.now()))

    savedata()


@bot.command()
@commands.has_permissions(administrator=True)
async def forceupdate(ctx):
    await refreshdata()
    print("data refreshed by event forceupdate at " + str(datetime.datetime.now()))
    url = bot.get_user(355004590602846208).avatar.url
    embed = discord.Embed(
        title="Twilight Dawn Developer API",
        description="Updated local serverinfo api data.\n"
                    "\n"
                    "Available on: `https://twilightdawnapi.pagekite.me/api/v1/serverinfo`"
    )
    embed.set_footer(icon_url=url, text="Developed by kiisuhh#2750 | hosted by lunox")

    await ctx.reply(embed=embed)

@bot.event
async def on_ready():
    print("connected")
    while True:
        await refreshdata()
        print("data refreshed by event hourly at " + str(datetime.datetime.now()))
        await asyncio.sleep(60*60)

@bot.event
async def on_member_ban(user, server):
    await refreshdata()
    print("data refreshed by event on_member_ban at " + str(datetime.datetime.now()))

@bot.event
async def on_member_unban(user, server):
    await refreshdata()
    print("data refreshed by event on_member_unban at " + str(datetime.datetime.now()))

@bot.event
async def on_member_join(member):
    await refreshdata()
    print("data refreshed by event on_member_join at " + str(datetime.datetime.now()))

@bot.event
async def on_member_remove(member):
    await refreshdata()
    print("data refreshed by event on_member_remove at " + str(datetime.datetime.now()))

@bot.event
async def on_guild_role_create(role):
    await refreshdata()
    print("data refreshed by event on_guild_role_create at " + str(datetime.datetime.now()))

@bot.event
async def on_guild_role_deleted(role):
    await refreshdata()
    print("data refreshed by event on_guild_role_deleted at " + str(datetime.datetime.now()))

@bot.event
async def on_guild_channel_create(channel):
    await refreshdata()
    print("data refreshed by event on_guild_channel_create at " + str(datetime.datetime.now()))

@bot.event
async def on_guild_channel_deleted(channel):
    await refreshdata()
    print("data refreshed by event on_guild_channel_deleted at " + str(datetime.datetime.now()))



def loaddata():
    global fulldata
    with open("data.json", "r") as f:
        fulldata = json.load(f)


def savedata():
    global fulldata
    with open("data.json", "w") as f:
        json.dump(fulldata, f, indent=4)


bot.run(os.getenv("TOKEN"))
