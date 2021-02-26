import discord
from discord.ext import commands 
import asyncio

class CAH(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(name='start', aliases=['s'], help='Starts a round of CAH.')
  async def start(self, ctx):
    em = discord.Embed(title='Started a game!', color=ctx.author.color)
    em.add_field(name= 'How to Join', value='React with ➕ to join. if you are the gamemaster, you may react with ⏯️ to start the game.')
    msg = await ctx.send(embed=em)
    await msg.add_reaction('➕')
    await msg.add_reaction('➖')
    await msg.add_reaction('⏯️')




  
















  @commands.command(name='end')
  async def end(self, ctx):
    msg = await ctx.send('The game was ended.')




def setup(client):
  client.add_cog(CAH(client)) 