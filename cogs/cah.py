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
      

    #functions:
    #def add_to_game():
      #code shit that adds user to the db/records where the bot can call upon/dm them with their cards and displays them in the lb. making this a function cuz then it's ez later to just on_reactions_add: add_to_game. ez w.


    #def remove_from_game():
      #same as above but removing

    #def update_trivia_scores():
      #literally look at the Name

    #def get_trivia_scores():
      #gets trivia scores lmao

    #def get_white_cards():
      #opens a json for white compile


    #def get_black_cards():
      #opens the json for black cards
    



  

  @commands.command(name='end')
  async def end(self, ctx):
    em = discord.Embed(title="The game was ended.", description="Hope all had some good fun! ;)", color=ctx.author.color)
    await ctx.send(em=embed)

  




def setup(bot):
  bot.add_cog(CAH(bot)) 