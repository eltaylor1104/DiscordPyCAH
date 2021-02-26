import discord
from discord.ext import commands 
import asyncio
import asyncpraw
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
      msg = await ctx.send(content = f"{member.mention} to accept {ctx.author.mention}'s beer invite. React with beer to this embed!", embed = em)
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
  async def meme(self, ctx):
      reddit  = asyncpraw.Reddit(client_id = "l5KErE-xWO6ugA", client_secret = "yHowpfj4lWcAhkLRkRRduQBMVK-WcA", username = "eltaylor1104", password = "Stingers1*", user_agent = "ios:com.memebot.myredditapp:2021.06.0.307548 (by u/eltaylor1104)")
      subreddit = await  reddit.subreddit("memes")
 
      all_subs = []
 
      async for submission in subreddit.hot(limit=300):
              all_subs.append(submission)
              random_sub = random.choice(all_subs)
              name = random_sub.title
              url = random_sub.url
              score = random_sub.score
 
 
      embed = discord.Embed(
            title = f'{name}',
            url = f'{url}',
            color = int("0x{:06x}".format(random.randint(0, 0xFFFFFF)), 16)
        )
 
 
      embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
      embed.set_image(url=url)
      embed.set_footer(text=f"👍 {score}")
 
      await ctx.send(embed=embed)
def setup(client):
  client.add_cog(Troll(client)) 