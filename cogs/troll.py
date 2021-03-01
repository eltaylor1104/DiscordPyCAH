import discord
from discord.ext import commands 
import asyncio
import asyncpraw
import aiohttp
import random
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


  @commands.command(aliases=['memes'])
  async def meme(self, ctx):
      async with aiohttp.ClientSession() as cs:
          async with cs.get('https://www.reddit.com/r/memes/random/.json') as r:
              res = await r.json()

              image= res[0]['data']['children'][0]['data']['url']
              permalink= res[0]['data']['children'][0]['data']['permalink']
              url = f'https://reddit.com{permalink}'
              title = res[0]['data']['children'][0]['data']['title']
              ups = res[0]['data']['children'][0]['data']['ups']
              downs = res[0]['data']['children'][0]['data']['downs']
              comments = res[0]['data']['children'][0]['data']['num_comments']

              embed = discord.Embed(colour=discord.Color.blurple(), title=title, url=url)
              embed.set_image(url=image)
              embed.set_footer(text=f"🔺 {ups} 💬 {comments}")
              await ctx.send(embed=embed, content=None)



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
def setup(client):
  client.add_cog(Troll(client)) 