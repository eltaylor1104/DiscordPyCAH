import discord
from discord.ext import commands 
import asyncio
import asyncpraw
import aiohttp
import random
from random import randint
from random import choice
from urllib.parse import quote_plus
from collections import deque


#CREDIT TO BobDotCom on GitHub and Discord for part of this code, primarily the reddit commands. THAT IS NOT MY CODE!

acceptableImageFormats = [".png",".jpg",".jpeg",".gif",".gifv",".webm",".mp4","imgur.com"]
memeHistory = deque()
memeSubreddits = ["BikiniBottomTwitter", "memes", "2meirl4meirl", "deepfriedmemes", "MemeEconomy"]
async def getSub(self, ctx, subreddit):
    if True:
      url = f"https://reddit.com/r/{subreddit}/random.json?limit=1"
      async with aiohttp.ClientSession() as session:
        async with session.get(f"https://reddit.com/r/{subreddit}/random.json?limit=1") as r:
          res = await r.json()
          s = ""
          subredditDict = dict(res[0]['data']['children'][0]['data'])
          if subredditDict['over_18'] and not ctx.channel.is_nsfw():
              embed = discord.Embed(title="Thats an NSFW subreddit!", description="To get an image from this subreddit, please use this command again in an NSFW channel", timestamp=ctx.message.created_at, color=discord.Color.red())
              await ctx.send(embed=embed)
              return
          embed = discord.Embed(title = f"{subredditDict['title']}", description = f"{subredditDict['subreddit_name_prefixed']}", url =  f"https://reddit.com{subredditDict['permalink']}", timestamp=ctx.message.created_at)
          
          if subredditDict['selftext'] != "":
              embed.add_field(name = "Post Content:", value = subredditDict['selftext'])
          if subredditDict['url'] != "":
              embed.set_image(url = subredditDict['url'])
          embed.set_footer(text=f"🔺 {subredditDict['ups']} | Author: {subredditDict['author']}")
          if subredditDict['selftext'] != "&amp;#x200B;":
                await ctx.send(embed = embed)
          else:
                await ctx.send("Annoying error with reddit being stupid please re use the command thanks")
    else:
      try: 
        return await ctx.send("_{}! ({})_".format(str(subredditDict['message']), str(subredditDict['error'])))
      except:
        return await ctx.send("Error")
async def getSubs(self, ctx, sub):
      """Get stuff from requested sub"""
      async with aiohttp.ClientSession() as session:
          async with session.get(f"https://www.reddit.com/r{sub}/hot.json?limit=450") as response:
              request = await response.json()
                  
      attempts = 1
      while attempts < 5:
          if 'error' in request:
              print("failed request {}".format(attempts))
              await asyncio.sleep(2)
              async with aiohttp.ClientSession() as session:
                  async with session.get(f"https://www.reddit.com/r/{sub}/hot.json?limit=450") as response:
                      request = await response.json()
              attempts += 1
          else:
              index = 0
              for index, val in enumerate(request['data']['children']):
                  if val['data']["over_18"] == True:
                      if not ctx.channel.is_nsfw():
                          return await ctx.send("Thats an nsfw reddit, nonono")
                  if 'url' in val['data']:
                      print(val['data'])
                      url = val['data']['url']
                      thetitle = val['data']['title']
                      thereddit = val['data']['subreddit_name_prefixed']
                      upvotes = val['data']['ups']
                      link = val['data']['permalink']
                      if val['data']['selftext'] != "":
                          selftext = val['data']['selftext']
                      urlLower = url.lower()
                      accepted = False
                      for j, v, in enumerate(acceptableImageFormats): #check if it's an acceptable image
                          if v in urlLower:
                              accepted = True
                      if accepted:
                          if url not in memeHistory:
                              memeHistory.append(url)  #add the url to the history, so it won't be posted again
                              if len(memeHistory) > 500: #limit size
                                  memeHistory.popleft() #remove the oldest

                              break #done with this loop, can send image
              subredditDict = dict(request['data']['children'][0]['data'])
              embed = discord.Embed(title=f"{thereddit}", description=f"{thetitle}", url=f"{link}", footer=f"🔺 {upvotes}", timestamp=ctx.message.created_at)
              embed.set_image(url=memeHistory[len(memeHistory) - 1])
              await ctx.send(embed=embed) #send the last image
              return
      await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))

class Troll(commands.Cog):
  def __init__(self, client):
    self.client = client


  @commands.command(help='Creates a countdown to Rickroll Message.')
  @commands.has_permissions(manage_messages=True)
  async def rick(self, ctx, time:int):
    await ctx.message.delete()
    if time > 1000:
        await ctx.send("O-oni-chan... I can't wait that long-")
        return
    count = time
    one = await ctx.send(f"Rickrolling you in {count}")
    for i in range(time):
        count -= 1
        await asyncio.sleep(1)
        await one.edit(content=f"Rickrolling you in {count}")
    await one.edit(content="https://youtu.be/dQw4w9WgXcQ")



  #Beer 
  @commands.command()
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def beer(self, ctx, member : discord.Member = None, *, reason = None):
      if member is None:
          return await ctx.send(f"{ctx.author.name}'s party!! :tada::beer:")
      
      if member == self.client.user:
          return await ctx.send("drinks beer with you* :beers:")
      
      em = discord.Embed(title = "Beer Invitation :beer:", color = ctx.author.color)
      em.add_field(name = "Member:", value = f"{member.mention}")
      em.add_field(name=  "Inviter:", value = f"{ctx.author.mention}")
      if reason is not None:
          em.add_field(name = "Reason:", value = f"`{reason}`")
      msg = await ctx.send(content = f"{member.mention} to accept {ctx.author.mention}'s beer invite, react with beer to this embed!", embed = em)
      await msg.add_reaction("<:PepeBeer:814030852605476874>")

      def check(reaction, user):
          return user == member and str(reaction.emoji) == "<:PepeBeer:814030852605476874>"

      try:
          reaction, user = await self.client.wait_for('reaction_add', timeout=120.0, check=check)

      except asyncio.TimeoutError:
          msg=(f"{member.mention} didn't accept the beer in time!")
          await ctx.channel.send(msg)

      else:
          successEmbed = discord.Embed(title = "<a:success:814032076138348584> Beer Successful!", color = ctx.author.color, description = f"{member.name} and {ctx.author.name} are enjoing a lovely beer :beers:!").add_field(name = "Member:", value = f"{member.mention}").add_field(name=  "Inviter:", value = f"{ctx.author.mention}")
          return await msg.edit(embed = successEmbed, content = f"{member.mention} accepted the beer!")






  @commands.command()
  @commands.guild_only()
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def trash(self, ctx, user: discord.Member = None):
      """It's Trash smh! """
      
      if user == None:
          user = ctx.author

      await ctx.trigger_typing()
      url = user.avatar_url_as(format="jpg")
      async with aiohttp.ClientSession() as cs:
          async with cs.get("https://nekobot.xyz/api/imagegen type=trash&url=%s" % (url,)) as r:
              res = await r.json()
              embed = discord.Embed(
                  title = "Trash SMH!",
                  color=0x5f3fd8

              )
              embed.set_image(url=res['message'])
              embed.set_author(name = f"{user.name}" , icon_url = user.avatar_url)
              embed.set_footer(text=f'Requested by {user.name}',icon_url = user.avatar_url)
      await ctx.send(embed=embed)
     
      
  @commands.command(aliases=['st','shower'])
  @commands.cooldown(1, 1, commands.BucketType.channel)
  async def showerthought(self, ctx):
    async with ctx.typing():
      if True:
        async with aiohttp.ClientSession() as session:
          async with session.get("https://www.reddit.com/r/showerthoughts/hot.json?limit=450") as response:
              request = await response.json()

        attempts = 1
        while attempts < 5:
          if 'error' in request:
              print("failed request {}".format(attempts))
              await asyncio.sleep(2)
              async with aiohttp.ClientSession() as session:
                  async with session.get("https://www.reddit.com/r/showerthoughts/hot.json?limit=450") as response:
                      request = await response.json()
              attempts += 1
          else:
              index = 0

              for index, val in enumerate(request['data']['children']):
                  if 'title' in val['data']:
                      url = val['data']['title']
                      urlLower = url.lower()
                      accepted = False
                      if url == "What Is A Showerthought?":
                          accepted = False
                      elif url == "Showerthoughts is looking for new moderators!":
                          accepted = False
                      elif url == "IMPORTANT PSA: No, you did not win a gift card.":
                          accepted = False
                      else:
                          accepted = True
                      if accepted:
                          if url not in memeHistory:
                              memeHistory.append(url)
                              if len(memeHistory) > 63:
                                  memeHistory.popleft()

                              break
              embed = discord.Embed(title=f"Showerthought", timestamp=ctx.message.created_at, description=memeHistory[len(memeHistory) - 1],color=discord.Color.blurple())
              await ctx.send(embed=embed)
              return
        await ctx.send("_{}! ({})_".format(str(request['message']), str(request['error'])))
  @commands.command(aliases=["ph"])
  @commands.cooldown(1, 1, commands.BucketType.channel)
  async def programmerhumor(self, ctx):
    """Get an image from the ProgrammerHumor subreddit."""
    async with ctx.typing():
      await getSub(self, ctx, 'ProgrammerHumor')
      
  @commands.command(aliases=["r"])
  @commands.cooldown(1, 1, commands.BucketType.channel)
  async def reddit(self, ctx, arg):
    """Get an image from a subreddit."""
    async with ctx.typing():
      await getSub(self, ctx, arg)

  @commands.command()
  @commands.cooldown(1, 1, commands.BucketType.channel)
  async def meme(self, ctx):
    """Memes from various subreddits"""
    async with ctx.typing():
      if True:
        await getSub(self, ctx, choice(memeSubreddits))
      else:
        async with aiohttp.ClientSession() as session:
          async with session.get("https://www.reddit.com/r/{0}/hot.json?limit=450".format(random.choice(memeSubreddits))) as response:
              request = await response.json()

        attempts = 1
        while attempts < 5:
          if 'error' in request:
              print("failed request {}".format(attempts))
              await asyncio.sleep(2)
              async with aiohttp.ClientSession() as session:
                  async with session.get("https://www.reddit.com/r/{0}/hot.json?limit=450".format(random.choice(memeSubreddits))) as response:
                      request = await response.json()
              attempts += 1
          else:
              index = 0

              for index, val in enumerate(request['data']['children']):
                  if 'url' in val['data']:
                      url = val['data']['url']
                      urlLower = url.lower()
                      accepted = False
                      for j, v, in enumerate(acceptableImageFormats): 
                          if v in urlLower:
                              accepted = True
                      if accepted:
                          if url not in memeHistory:
                              memeHistory.append(url)  
                              if len(memeHistory) > 500: 
                                  memeHistory.popleft() 

                              break 
              embed = discord.Embed(title=f"Meme", timestamp=ctx.message.created_at,color=ctx.author.color)
              embed.set_image(url=memeHistory[len(memeHistory) - 1])
              await ctx.send(embed=embed)
              return
        await ctx.send(url="_{}! ({})_".format(str(request['message']), str(request['error'])))
def setup(client):
  client.add_cog(Troll(client)) 