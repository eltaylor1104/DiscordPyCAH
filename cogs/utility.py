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
  @commands.command(name="ping")
  async def ping_(self, ctx):
    msg = await ctx.send("Pinging...")
    await msg.edit(content=f":ping_pong: Pong! `{round(self.bot.latency * 1000)}ms`")

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
     file = json.load(open(r"json//snipe-dict.json", "r"))
     if not msg.author.bot:
      if not str(msg.guild.id) in file:
          file[str(msg.guild.id)] = {}
      file[str(msg.guild.id)]["user-id"] = msg.author.id
      file[str(msg.guild.id)]["content"] = msg.content
      json.dump(file, open(r"json//snipe-dict.json", "w"), indent=4)

  @commands.command()
  @cooldown(1, 5, BucketType.user)
  async def snipe(self, ctx):
     file = json.load(open(r"json//snipe-dict.json", "r"))
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
     file = json.load(open(r"json//editsnipe-dict.json", "r"))
     if not msg_before.author.bot:
      if not str(msg_before.guild.id) in file:
          file[str(msg_before.guild.id)] = {}
      file[str(msg_before.guild.id)]["user-id"] = msg_before.author.id
      file[str(msg_after.guild.id)]["before-content"] = msg_before.content
      file[str(msg_after.guild.id)]["after-content"] = msg_after.content
      json.dump(file, open(r"json//editsnipe-dict.json", "w"), indent=4)

  @commands.command()
  @cooldown(1, 5, BucketType.user)
  async def editsnipe(self, ctx):
      file = json.load(open(r"json//editsnipe-dict.json", "r"))
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
    @commands.command(hidden=True)
    @commands.is_owner()
    async def blacklist(self,ctx,action,user_id,time_amount='Permanent',*,reason=None):
        user_id = int(user_id)
        with open(r"json//blacklisted.json",'r') as f:
            data = json.load(f)
        data['users'] = data['users'] or []
        if action == "add":
            data['users'].append(user_id)
        elif action == 'remove':
            data['users'].remove(user_id)
        self.client.blacklisted = data["users"]
        with open(r"json//blacklisted.json",'w') as f:
            json.dump(data,f,indent=4)
        if not time_amount.lower() in ['permanent',"forever"]:
            time_amount = f"**{time_amount}** \nOnce this time is up, you may make an appeal to my developer."
        else:
            time_amount = f"**{time_amount}**"
        try:
            user = self.client.get_user(user_id)
            if action == "add":
                embed = discord.Embed(title="You've been blacklisted!",description=f"This means you will not be able to use the bot. If you would like to appeal this, or if you think this is a mistake, please contact my developer {self.client.get_user(self.client.owner_ids[0])}.",color=discord.Color.red())
                embed.add_field(name='Time',value=time_amount)
                embed.add_field(name='Reason',value=reason or 'None specified')
                await user.send(embed=embed)
                await ctx.send(f'Successfully blacklisted {user}')
            elif action == 'remove':
                await user.send('You have been removed from the blacklist. You may use the bot now.')
                await ctx.send(f'Successfully unblacklisted {user}')
        except:
            await ctx.send('failed')

def setup(bot):
  bot.add_cog(Util(bot))    
