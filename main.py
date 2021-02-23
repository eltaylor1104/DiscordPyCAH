import discord
import os
import random
import json
import logging
import keep_alive
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix = 'c!')


#Status Shit
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Cards Against Humanity!'))
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


@client.command()
async def ping(ctx):
    if round(client.latency * 1000) <= 50:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pong! The ping is **{round(client.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(client.latency * 1000) <= 100:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pong! The ping is **{round(client.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(client.latency * 1000) <= 200:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pong! The ping is **{round(client.latency *1000)}** milliseconds!", color=0xff6600)
    else:
        embed=discord.Embed(title="PING", description=f":ping_pong: Pong! The ping is **{round(client.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.send(embed=embed)

keep_alive.keep_alive()
client.run(TOKEN)