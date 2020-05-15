import coc
import traceback

import discord
from discord.ext import commands

# Read info at Discord Developer Portal and Clash of Clans Developer Portal before use!

'''
Store authentication info in separate file:
line 1: CoC dev username
line 2: CoC dev password
line 3: DC info channel ID
line 4: DC bot OAUTH2 token
line 5: Your clan's tag
'''
with open("../orabot_food.txt") as f:
    auth = f.readlines()
auth = [x.strip() for x in auth] 

clan_tag = auth[4] # Tag of the clan that you want to follow.
coc_client = coc.login(auth[0], auth[1], key_count=5, key_names="Bot key", client=coc.EventsClient,)

bot = commands.Bot(command_prefix="!")
INFO_CHANNEL_ID = int(auth[2]) # ID of the info channel where the bot will post messages.

@coc_client.event
async def on_clan_member_versus_trophies_change(old_trophies, new_trophies, player):
	await bot.get_channel(INFO_CHANNEL_ID).send(
        "{0.name}-nek jelenleg {1} versus trófeája van".format(player, new_trophies))

@bot.command()
async def szia(ctx):
    await ctx.send("Szia!")

@bot.command()
async def parancsok(ctx):
    await ctx.send("!szia, !hosok \{player_tag\}, !tagok")

@bot.command()
async def hosok(ctx, player_tag):
    player = await coc_client.get_player(player_tag)

    to_send = ""
    for hero in player.heroes:
        to_send += "{}: Lv {}/{}\n".format(str(hero), hero.level, hero.max_level)

    await ctx.send(to_send)

@bot.command()
async def tagok(ctx):
    members = await coc_client.get_members(clan_tag)

    to_send = "A tagok:\n"
    for player in members:
        to_send += "{0} ({1})\n".format(player.name, player.tag)

    await ctx.send(to_send)

coc_client.add_clan_update(
    [clan_tag], retry_interval=60
)
coc_client.start_updates()

bot.run(auth[3])
