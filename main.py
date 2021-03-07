import discord
import os
import random
import json
import logging
from discord.ext import commands
from pathlib import Path
import keep_alive
from discord.ext import commands
from ratelimit import limits

TOKEN = os.getenv('DISCORD_TOKEN')
cwd = Path(__file__).parents[0]
cwd = str(cwd)




def get_prefix(client, message):
	if not message.guild:
		return ['C!', 'c!']
	with open(r'json//prefixes.json', 'r') as f:
		prefixes = json.load(f)
	try:
		x = prefixes[str(message.guild.id)]
	except:
		x = ["C.","c."]
	if x == []:
		x += ["C.","c.",]
	if not client.user.id == 815636133324914728:
		return commands.when_mentioned_or(*x)(client, message)
	else:
		y = ['C,','c,',]
		return commands.when_mentioned_or(*y)(client, message)


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=get_prefix,intents=intents,case_insensitive = True)
try:
    with open(r'json//blacklisted.json','r') as f:
        data = json.load(f)
    bot.blacklisted = data['users']
except:
    bot.blacklisted = []
    print('Blacklist not loaded')

def get_prefix(client,message):

    with open(r"json//prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]







@bot.command()
async def invite(ctx):
  embed = discord.Embed(title='pls invite me I am desperate. k thx bai', color=ctx.author.color, description=f"[Click here to invite me to your server.](https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot)")
  await ctx.send(embed=embed)


@bot.event
async def on_guild_join(guild):


    with open(r"json//prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "c!"

    with open(r"json//prefixes.json", "w") as f:
        json.dump(prefixes,f)


@bot.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):

    with open(r"json//prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open(r"json//prefixes.json", "w") as f:
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