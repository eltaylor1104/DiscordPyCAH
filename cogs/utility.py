import discord
from discord.ext import commands 
from discord.ext.commands import bot_has_permissions, has_permissions, cooldown, BucketType
import json
import asyncio
import random

class Util(commands.Cog):

  def __init__(self, bot):
    self.bot = bot


#events
  @commands.Cog.listener()
  async def on_ready(self):
    print('Bot is online. Yeeyee!')
#commands
  @commands.command()
  async def ping(self, ctx):
      await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')
  

  @commands.command(aliases=["av"])
  @cooldown(1, 1, BucketType.user)
  async def avatar(self, ctx, member: discord.Member = None):

        if member == None:
            member = ctx.author
        embed = discord.Embed(
            title=f"{member.name}'s avatar",
            colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        embed.set_image(url=member.avatar_url)
        embed.set_footer(
            text=
            f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

  @commands.Cog.listener()
  async def on_message_delete(self, msg):
     file = json.load(open(r"snipe-dict.json", "r"))
     if not msg.author.bot:
      if not str(msg.guild.id) in file:
          file[str(msg.guild.id)] = {}
      file[str(msg.guild.id)]["user-id"] = msg.author.id
      file[str(msg.guild.id)]["content"] = msg.content
      json.dump(file, open(r"snipe-dict.json", "w"), indent=4)

  @commands.command()
  @cooldown(1, 5, BucketType.user)
  async def snipe(self, ctx):
     file = json.load(open(r"snipe-dict.json", "r"))
     if not str(ctx.guild.id) in file:
         return await ctx.send("There's nothing to snipe!")
    
     user_id = file[str(ctx.guild.id)]["user-id"]
     content = file[str(ctx.guild.id)]["content"]
     user = await self.bot.fetch_user(user_id)    
     embed = discord.Embed(color=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), timestamp=ctx.message.created_at)
     embed.set_author(name=user, icon_url=user.avatar_url)
     embed.description = f"{content}"
     embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
     await ctx.send(embed=embed)

  @snipe.error
  async def snipe_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      em = discord.Embed(title=random.choice(["Take a chill pill", "Slow it down, C'mon", "Hold your horses"]), colour=discord.Colour.blurple())
      em.description = f"You'll be able to use the `{ctx.command.name}` command again in **{round(error.retry_after)} second(s)**\nThe default cooldown is `5s`"
      await ctx.message.reply(embed=em)
    else:
      await ctx.send(f"**An Unknown Error Occurred**\n\nAn unknown error occured in the `{ctx.command.name}` command.")

  @commands.Cog.listener()
  async def on_message_edit(self, msg_before, msg_after):
     file = json.load(open(r"editsnipe-dict.json", "r"))
     if not msg_before.author.bot:
      if not str(msg_before.guild.id) in file:
          file[str(msg_before.guild.id)] = {}
      file[str(msg_before.guild.id)]["user-id"] = msg_before.author.id
      file[str(msg_after.guild.id)]["before-content"] = msg_before.content
      file[str(msg_after.guild.id)]["after-content"] = msg_after.content
      json.dump(file, open(r"editsnipe-dict.json", "w"), indent=4)

  @commands.command()
  @cooldown(1, 5, BucketType.user)
  async def editsnipe(self, ctx):
      file = json.load(open(r"editsnipe-dict.json", "r"))
      if not str(ctx.guild.id) in file:
          return await ctx.send("There's nothing to snipe!")
    
      user_id = file[str(ctx.guild.id)]["user-id"]
      before_content = file[str(ctx.guild.id)]["before-content"]
      after_content = file[str(ctx.guild.id)]["after-content"]
      user = await self.bot.fetch_user(user_id)    
      embed = discord.Embed(colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),timestamp=ctx.message.created_at)
      embed.set_author(name=user, icon_url=user.avatar_url)
      embed.description = f"**Before**:\n{before_content}\n\n**After**:\n{after_content}"
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)

  @editsnipe.error
  async def editsnipe_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      em = discord.Embed(title=random.choice(["Take a chill pill", "Slow it down, C'mon", "Hold your horses"]), colour=discord.Colour.blurple())
      em.description = f"You'll be able to use the `{ctx.command.name}` command again in **{round(error.retry_after)} second(s)**\nThe default cooldown is `5s`"
      await ctx.message.reply(embed=em)
    else:
      await ctx.send(f"**An Unknown Error Occurred**\n\nAn unknown error occured in the `{ctx.command.name}` command.)")


def setup(bot):
  bot.add_cog(Util(bot))    
