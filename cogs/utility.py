import discord
from discord.ext import commands 

class Util(commands.Cog):

  def __init__(self, client):
    self.client = client


#events
  @commands.Cog.listener()
  async def on_ready(self):
    print('Bot is online. Yeeyee!')
#commands
  @commands.command()
  async def ping(self, ctx):
      await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

def setup(client):
  client.add_cog(Util(client))    
