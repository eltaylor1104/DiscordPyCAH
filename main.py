import discord
import os
import random
import json
import logging
import rickroll_detector
from discord.ext import commands
from rickroll_detector import find_rickroll



from pathlib import Path
import keep_alive
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')
cwd = Path(__file__).parents[0]
cwd = str(cwd)






def get_prefix(client,message):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]



bot = commands.Bot(command_prefix=get_prefix,intents = discord.Intents.default())


RICKROLL_FOUND_MESSAGE = "⚠️Rickroll Alert⚠️"


@bot.event
async def on_message(msg):
    for i in msg.content.split(" "):
        i = i.replace("<","").replace(">", "") #Removes <> that could be used to hide embeds
        if "https://" in i and find_rickroll(i):
            await msg.reply(RICKROLL_FOUND_MESSAGE)
            break

    await bot.process_commands(msg)

@bot.event
async def on_guild_join(guild):


    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "c!"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)


@bot.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)    

    await ctx.send(f"The prefix was changed to {prefix}")


  
#Status Shit
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='cards against humanity'))
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
#cogs
@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')
  await ctx.send(f'{extension} successfully loaded')

# cog unloader command
@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  await ctx.send(f'{extension} successfully unloaded.')

# cog reloader command, unload then load extenion
@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  bot.load_extension(f'cogs.{extension}')
  await ctx.send(f'{extension} successfully reloaded.')






for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')



keep_alive.keep_alive()
bot.run(TOKEN)