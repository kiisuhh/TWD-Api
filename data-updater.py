import json
import os
import colorama
from colorama import Fore, Back, Style
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import datetime
import sys
import pathlib
import time

os.system('cls')
print(f"{Fore.CYAN}{Style.BRIGHT}     __     __                            __     __         ")
print(f" ___/ /__ _/ /____ _  ____  __ _____  ___/ /__ _/ /____ ____")
print(f"/ _  / _ `/ __/ _ `/ /___/ / // / _ \/ _  / _ `/ __/ -_) __/")
print(f"\_,_/\_,_/\__/\_,_/        \_,_/ .__/\_,_/\_,_/\__/\__/_/   ")
print(f"                              /_/    _____                  ")
print(f"                              __  __/__  /                  ")
print(f"                              | |/ / ___/                   ")
print(f"                              |___/____/        {Fore.WHITE}")
print()

load_dotenv()
fulldata = dict
fulldatav2 = dict

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
    async for ban in guild.bans(limit=5000):
        bancount += 1
        #fixed by forniter1337 aka foxon heheheha
    for softbans in guild.get_role(874028969920438362).members:
        bancount += 1

    ageindays = (datetime.datetime.now().date() - guild.created_at.date()).days

    bots = 0
    for member in guild.get_role(872089246729666560).members:
        bots += 1

    # v1
    fulldata["Serverstats"]["membercount"] = membercount
    fulldata["Serverstats"]["rolecount"] = rolecount
    fulldata["Serverstats"]["boosts"] = boostcount
    fulldata["Serverstats"]["twilights"] = twilightcount
    fulldata["Serverstats"]["channel"] = channelcount
    fulldata["Serverstats"]["bans"] = bancount
    fulldata["Serverstats"]["days"] = ageindays
    fulldata["Serverstats"]["bots"] = bots

    # v2
    fulldatav2["ServerStats"]["membercount"] = membercount
    fulldatav2["ServerStats"]["rolecount"] = rolecount
    fulldatav2["ServerStats"]["boosts"] = boostcount
    fulldatav2["ServerStats"]["twilights"] = twilightcount
    fulldatav2["ServerStats"]["channel"] = channelcount
    fulldatav2["ServerStats"]["bans"] = bancount
    fulldatav2["ServerStats"]["days"] = ageindays
    fulldatav2["ServerStats"]["bots"] = bots

    #print("data updated at " + str(datetime.datetime.now()))

    savedata()


@bot.command()
@commands.has_permissions(administrator=True)
async def forceupdate(ctx):
    await refreshdata()
    await updateteamassets()
    print("data refreshed by event forceupdate at " + str(datetime.datetime.now()))
    url = bot.get_user(355004590602846208).avatar.url
    embed = discord.Embed(
        title="Twilight Dawn Developer API",
        description="Updated local serverinfo api data.\n"
                    "\n"
                    "Available on: `https://twilightdawnapi.pagekite.me/api/v1/serverinfo`"
    )
    embed.set_footer(icon_url=url, text="Developed by hiroyukisu#2750 | hosted by lunox")

    await ctx.reply(embed=embed)

updatetimes = 0

async def last_updated():
    while True:
        global updatetimes
        modTime = datetime.datetime.fromtimestamp(os.path.getmtime('./datav2.json'))
        await asyncio.sleep(0.5)
        datetime_now = datetime.datetime.now()
        #print(modTime)
        modTime = datetime_now - modTime
        modTimesec = modTime.total_seconds()
        #print(datetime_now)

        #print(modTime)
        if modTimesec >= 60:
            if modTimesec >= 3600:
                print(f"Last updated {modTime.seconds // 3600} hour(s), {modTime.seconds // 60 % 60} minute(s) and {modTime.seconds % 60} second(s) ago | totally updated {updatetimes} times                                                    ", end="\r")
            else:
                print(f"Last updated {modTime.seconds / 60} minutes and {modTime.seconds % 60} seconds ago | totally updated {updatetimes} times                                                     ", end="\r")
        else:
            print(f"Last updated {modTime.seconds} seconds ago | totally updated {updatetimes} times                                                    ", end="\r")
            #print(f"Last updated {modTime.seconds} seconds ago | totally updated {updatetimes} times")
        await asyncio.sleep(0.5)

async def refresh():
    while True:
        global updatetimes
        updatetimes += 1
        await refreshdata()
        await updateteamassets()
        #print("data refreshed by event hourly at " + str(datetime.datetime.now()))
        #print('|', end='')
        #sys.stdout.flush()
        await asyncio.sleep(10)

async def loop_presence():
    while True:
        botstatusmessage2 = "💸 Moneyboy 💸"
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=botstatusmessage2))
        await asyncio.sleep(10)
        botstatusmessage1 = f"the stats | already updated {updatetimes} times since online"
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=botstatusmessage1))
        await asyncio.sleep(10)

async def test():
    bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="test"))

async def live():
    while True:
        import requests
        channelName = 'ac3_o'
        contents = requests.get('https://www.twitch.tv/' +channelName).content.decode('utf-8')
        #print(contents)
        if 'isLiveBroadcast' in contents:
            botstatusmessage3 = "Ace ist live"
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=botstatusmessage3,
                                                                url="https://www.twitch.tv/ac3_o"))
        else:
            await loop_presence()
            #await test()

@bot.event
async def on_ready():
    print(f"connected as {bot.user}")
    print()
    await asyncio.wait([last_updated(), refresh(), live()])

@bot.event
async def on_member_update(user, server):
    await refresh()
    #print("data refreshed by event on_member_update at " + str(datetime.datetime.now()))
    #print('|', end='')
    #sys.stdout.flush()

@bot.event
async def on_member_ban(user, server):
    await refresh()
    #print("data refreshed by event on_member_ban at " + str(datetime.datetime.now()))
    #print('|', end='')
    #sys.stdout.flush()

@bot.event
async def on_member_unban(user, server):
    await refresh()
    #print("data refreshed by event on_member_unban at " + str(datetime.datetime.now()))
    #print('|', end='')
    #sys.stdout.flush()

@bot.event
async def on_member_join(member):
    await refresh()
    #print("data refreshed by event on_member_join at " + str(datetime.datetime.now()))
    #print('|', end='')
    #sys.stdout.flush()

@bot.event
async def on_member_remove(member):
    await refresh()
    #print("data refreshed by event on_member_remove at " + str(datetime.datetime.now()))
    #print('|', end='')
    #sys.stdout.flush()

@bot.event
async def on_guild_role_create(role):
    await refresh()
    #print("data refreshed by event on_guild_role_create at " + str(datetime.datetime.now()))
    #print('|', end='')
    #sys.stdout.flush()

@bot.event
async def on_guild_role_deleted(role):
    await refresh()
    #print("data refreshed by event on_guild_role_deleted at " + str(datetime.datetime.now()))
    #print('|', end='')
    #sys.stdout.flush()

@bot.event
async def on_guild_channel_create(channel):
    await refresh()
    #print("data refreshed by event on_guild_channel_create at " + str(datetime.datetime.now()))
    #print('|', end='')
    #sys.stdout.flush()

@bot.event
async def on_guild_channel_deleted(channel):
    await refresh()
    #print("data refreshed by event on_guild_channel_deleted at " + str(datetime.datetime.now()))
    #print('|', end='')
    #sys.stdout.flush()

def loaddata():
    global fulldata
    global fulldatav2
    with open("data.json", "r") as f:
        fulldata = json.load(f)
    with open("datav2.json", "r") as f:
        fulldatav2 = json.load(f)


def savedata():
    global fulldata
    global fulldatav2
    with open("data.json", "w") as f:
        json.dump(fulldata, f, indent=4)
    with open("datav2.json", "w") as f:
        json.dump(fulldatav2, f, indent=4)


async def updateteamassets():
    loaddata()
    ace = bot.get_user(int(os.getenv("AceID")))
    reiswafl = bot.get_user(int(os.getenv("ReiswaflID")))
    penmon = bot.get_user(int(os.getenv("PenmonID")))
    azra = bot.get_user(int(os.getenv("azraID")))
    #vincent = bot.get_user(int(os.getenv("VincentID")))
    liv = bot.get_user(int(os.getenv("LIVID")))
    luca = bot.get_user(int(os.getenv("lucaID")))
    caro = bot.get_user(int(os.getenv("caroID")))
    Max = bot.get_user(int(os.getenv("MaxID")))
    Picosohn = bot.get_user(int(os.getenv("PicosohnID")))
    kasumi = bot.get_user(int(os.getenv("kasumiID")))
    #wasabi = bot.get_user(os.getenv("wasabiID"))
    Paulus = bot.get_user(int(os.getenv("PaulusID")))
    Teejay = bot.get_user(int(os.getenv("TeejayID")))
    Amelie = bot.get_user(int(os.getenv("AmelieID")))
    #faulig = bot.get_user(int(os.getenv("FauligID")))
    #lunix = bot.get_user(int(os.getenv("LunixID")))

    del fulldatav2["Team"]
    fulldatav2["Team"] = {}

    fulldatav2["Team"]["Ace"] = {}
    fulldatav2["Team"]["Ace"]["name"] = ace.name
    fulldatav2["Team"]["Ace"]["discriminator"] = ace.discriminator
    fulldatav2["Team"]["Ace"]["name_format"] = f"{ace.name}#{ace.discriminator}"
    fulldatav2["Team"]["Ace"]["Avatar"] = ace.avatar.replace(size=256).url
    if ace.banner is not None:
        fulldatav2["Team"]["Ace"]["Banner"] = ace.banner.url
    else:
        fulldatav2["Team"]["Ace"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["Reiswafl"] = {}
    fulldatav2["Team"]["Reiswafl"]["name"] = reiswafl.name
    fulldatav2["Team"]["Reiswafl"]["discriminator"] = reiswafl.discriminator
    fulldatav2["Team"]["Reiswafl"]["name_format"] = f"{reiswafl.name}#{reiswafl.discriminator}"
    fulldatav2["Team"]["Reiswafl"]["Avatar"] = reiswafl.avatar.replace(size=256).url
    if reiswafl.banner is not None:
        fulldatav2["Team"]["Reiswafl"]["Banner"] = reiswafl.banner.url
    else:
        fulldatav2["Team"]["Reiswafl"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["Penmon"] = {}
    fulldatav2["Team"]["Penmon"]["name"] = penmon.name
    fulldatav2["Team"]["Penmon"]["discriminator"] = penmon.discriminator
    fulldatav2["Team"]["Penmon"]["name_format"] = f"{penmon.name}#{penmon.discriminator}"
    fulldatav2["Team"]["Penmon"]["Avatar"] = penmon.avatar.replace(size=256).url
    if penmon.banner is not None:
        fulldatav2["Team"]["Penmon"]["Banner"] = penmon.banner.url
    else:
        fulldatav2["Team"]["Penmon"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["azra"] = {}
    fulldatav2["Team"]["azra"]["name"] = azra.name
    fulldatav2["Team"]["azra"]["discriminator"] = azra.discriminator
    fulldatav2["Team"]["azra"]["name_format"] = f"{azra.name}#{azra.discriminator}"
    fulldatav2["Team"]["azra"]["Avatar"] = azra.avatar.replace(size=256).url
    if azra.banner is not None:
        fulldatav2["Team"]["azra"]["Banner"] = azra.banner.url
    else:
        fulldatav2["Team"]["azra"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["LIV"] = {}
    fulldatav2["Team"]["LIV"]["name"] = liv.name
    fulldatav2["Team"]["LIV"]["discriminator"] = liv.discriminator
    fulldatav2["Team"]["LIV"]["name_format"] = f"{liv.name}#{liv.discriminator}"
    fulldatav2["Team"]["LIV"]["Avatar"] = liv.avatar.replace(size=256).url
    if liv.banner is not None:
        fulldatav2["Team"]["LIV"]["Banner"] = liv.banner.url
    else:
        fulldatav2["Team"]["LIV"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["luca"] = {}
    fulldatav2["Team"]["luca"]["name"] = luca.name
    fulldatav2["Team"]["luca"]["discriminator"] = luca.discriminator
    fulldatav2["Team"]["luca"]["name_format"] = f"{luca.name}#{luca.discriminator}"
    fulldatav2["Team"]["luca"]["Avatar"] = luca.avatar.replace(size=256).url
    if luca.banner is not None:
        fulldatav2["Team"]["luca"]["Banner"] = luca.banner.url
    else:
        fulldatav2["Team"]["luca"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["caro"] = {}
    fulldatav2["Team"]["caro"]["name"] = caro.name
    fulldatav2["Team"]["caro"]["discriminator"] = caro.discriminator
    fulldatav2["Team"]["caro"]["name_format"] = f"{caro.name}#{caro.discriminator}"
    fulldatav2["Team"]["caro"]["Avatar"] = caro.avatar.replace(size=256).url
    if caro.banner is not None:
        fulldatav2["Team"]["caro"]["Banner"] = caro.banner.url
    else:
        fulldatav2["Team"]["caro"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["Max"] = {}
    fulldatav2["Team"]["Max"]["name"] = Max.name
    fulldatav2["Team"]["Max"]["discriminator"] = Max.discriminator
    fulldatav2["Team"]["Max"]["name_format"] = f"{Max.name}#{Max.discriminator}"
    fulldatav2["Team"]["Max"]["Avatar"] = Max.avatar.replace(size=256).url
    if Max.banner is not None:
        fulldatav2["Team"]["Max"]["Banner"] = Max.banner.url
    else:
        fulldatav2["Team"]["Max"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["Picosohn"] = {}
    fulldatav2["Team"]["Picosohn"]["name"] = Picosohn.name
    fulldatav2["Team"]["Picosohn"]["discriminator"] = Picosohn.discriminator
    fulldatav2["Team"]["Picosohn"]["name_format"] = f"{Picosohn.name}#{Picosohn.discriminator}"
    fulldatav2["Team"]["Picosohn"]["Avatar"] = Picosohn.avatar.replace(size=256).url
    if Picosohn.banner is not None:
        fulldatav2["Team"]["Picosohn"]["Banner"] = Picosohn.banner.url
    else:
        fulldatav2["Team"]["Picosohn"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["kasumi"] = {}
    fulldatav2["Team"]["kasumi"]["name"] = kasumi.name
    fulldatav2["Team"]["kasumi"]["discriminator"] = kasumi.discriminator
    fulldatav2["Team"]["kasumi"]["name_format"] = f"{kasumi.name}#{kasumi.discriminator}"
    fulldatav2["Team"]["kasumi"]["Avatar"] = kasumi.avatar.replace(size=256).url
    if kasumi.banner is not None:
        fulldatav2["Team"]["kasumi"]["Banner"] = kasumi.banner.url
    else:
        fulldatav2["Team"]["kasumi"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["Paulus"] = {}
    fulldatav2["Team"]["Paulus"]["name"] = Paulus.name
    fulldatav2["Team"]["Paulus"]["discriminator"] = Paulus.discriminator
    fulldatav2["Team"]["Paulus"]["name_format"] = f"{Paulus.name}#{Paulus.discriminator}"
    fulldatav2["Team"]["Paulus"]["Avatar"] = Paulus.avatar.replace(size=256).url
    if Paulus.banner is not None:
        fulldatav2["Team"]["Paulus"]["Banner"] = Paulus.banner.url
    else:
        fulldatav2["Team"]["Paulus"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["Teejay"] = {}
    fulldatav2["Team"]["Teejay"]["name"] = Teejay.name
    fulldatav2["Team"]["Teejay"]["discriminator"] = Teejay.discriminator
    fulldatav2["Team"]["Teejay"]["name_format"] = f"{Teejay.name}#{Teejay.discriminator}"
    fulldatav2["Team"]["Teejay"]["Avatar"] = Teejay.avatar.replace(size=256).url
    if Teejay.banner is not None:
        fulldatav2["Team"]["Teejay"]["Banner"] = Teejay.banner.url
    else:
        fulldatav2["Team"]["Teejay"]["Banner"] = "Kein Banner Vorhanden"

    fulldatav2["Team"]["Amelie"] = {}
    fulldatav2["Team"]["Amelie"]["name"] = Amelie.name
    fulldatav2["Team"]["Amelie"]["discriminator"] = Amelie.discriminator
    fulldatav2["Team"]["Amelie"]["name_format"] = f"{Amelie.name}#{Amelie.discriminator}"
    fulldatav2["Team"]["Amelie"]["Avatar"] = Amelie.avatar.replace(size=256).url
    if Amelie.banner is not None:
        fulldatav2["Team"]["Amelie"]["Banner"] = Amelie.banner.url
    else:
        fulldatav2["Team"]["Amelie"]["Banner"] = "Kein Banner Vorhanden"


    savedata()






bot.run(os.getenv("TOKEN"))
