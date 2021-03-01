import discord
from discord.ext import commands 
import asyncio

class CAH(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='start', aliases=['s'], help='Starts a round of CAH.')
  async def start(self, ctx):
    em = discord.Embed(title='Started a game!', color=ctx.author.color)
    em.add_field(name= 'How to Join', value='React with ➕ to join. if you are the gamemaster, you may react with ⏯️ to start the game.')
    msg = await ctx.send(embed=em)
    await msg.add_reaction('➕')
    await msg.add_reaction('➖')
    await msg.add_reaction('⏯️')


  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    #channel = self.bot.get_channel(payload.message_id)
    guild = self.bot.get_guild(payload.guild_id)
    channel = discord.utils.get(guild.channels, id=payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    
  
      
  
    
    if payload.emoji.name == '➕':
      await channel.send('you added a plus sign')


    if payload.emoji.name == '➖':
      await channel.send('you added a minus')

      
    if payload.emoji.name == '⏯️':
      await channel.send('resoom')
      

    ## I have no fucking clue how to fill in these functions, but I wanted to have them, becuase once they are here shit gets a lot easier when you just have to call upon functions to do shit instead of keep rewriting xD


    




  

  @commands.command(name='end')
  async def end(self, ctx):
    em = discord.Embed(title="The game was ended.", description="Hope all had some good fun! ;)", color=ctx.author.color)
    await ctx.send(em=embed)

  




def setup(bot):
  bot.add_cog(CAH(bot)) 