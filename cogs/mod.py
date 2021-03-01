import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions, BadArgument

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #CREDIT: BobDotCom on github for the following Moderation commands. THESE ARE NOT MINE!!!

    @commands.command(aliases=['nick'], help="Change the nickname of a user.")
    @commands.has_guild_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member : discord.Member, *args):
        if member == None:
            await ctx.send('Give me a user please')
        elif member == ctx.guild.owner:
            await ctx.send('You cant name the owner!')
        else:
          try:
            x = ' '.join(map(str, args))
            await member.edit(nick=f'{x}')
            await ctx.send(f'{member.name} has been changed to {x}')
          except:
            await ctx.send("I cant")
    @commands.command()
    @has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member = None, *, reason = None):
        try:
            if member == None:
                embed = discord.Embed(title = ":x: Kick Failed!", color= ctx.author.color)
                embed.add_field(name = "Reason:", value = "Ping a user to kick them!")
                await ctx.send(embed = embed)
                return
            if member == ctx.author:
                em = discord.Embed(title = ':x: Kick Failed', color = ctx.author.color)
                em.add_field(name = 'Reason:', value = f"You can't kick yourself ;-;")
                em.add_field(name = "Next Steps:", value = "Try to kick someone else idunno")
                em.set_footer(text = "imagine kicking urself, couldn't be me!")
                await ctx.send(embed=  em)
                return
            try:
                await member.send(f"You were kicked in {ctx.guild.name}\nReason: `{reason}`\nModerator: `{ctx.author.name}`")
            except:
                pass
            await member.kick(reason = reason)
            em = discord.Embed(title = f":white_check_mark: Kick was successful!", color = ctx.author.color)
            em.add_field(name = f"Member:", value = f"`{member.name}`")
            em.add_field(name = "Reason: ", value = f"`{reason}`")
            em.add_field(name = "Moderator:", value = f"`{ctx.author.name}`")
            em.set_footer(text = f"{member.name} said bye!")
            await ctx.send(embed = em)
        except:
            em = discord.Embed(title = ":x: Kick Failed!", color = discord.Color.red())
            em.add_field(name = 'Reason', value =f"{member.mention} is a moderator or an admin!")
            em.add_field(name = "Hierarchy", value = "This could also be due to the hierarchy!")
            await ctx.send(embed = em)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title = ":x: Kick Failed!", color = ctx.author.color)
            em.add_field(name = "Reason:", value = "`Kick members Permission Missing!`")
            em.set_footer(text = "Imagine thinking you have the perms!")
            await ctx.send(embed = em)
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title = ":x: Kick Failed!", color = ctx.author.color)
            em.add_field(name = "Reason:", value = "`Ping a user to kick them!`")
            em.add_field(name=  "Usage:", value = "```diff\n+ c!kick @bonfire#6969 swear words\n- c!kick someonesName swearing\n```")
            em.set_footer(text = "Kick properly already!")
            await ctx.send(embed = em)
        
    async def createDiff(self, plusField, minusField):
        return f"""
        ```diff\n
        + {plusField}\n
        - {minusField}\n 
        ```
        """

    @commands.command(aliases=["giverole", "addr"])
    @has_permissions(manage_roles = True)
    async def addrole(self, ctx, member : discord.Member = None, role : discord.Role = None,*,reason = None):
        if member is None:
            embed = discord.Embed(title = ":x: Addrole Failed!", color= ctx.author.color)
            embed.add_field(name = "Reason:", value = "Ping a user to give them a role them!")
            embed.set_footer(text = "-_-")
            await ctx.send(embed = embed)
            return
        if role is None:
            embed = discord.Embed(title = ":x: Addrole Failed!", color= ctx.author.color)
            embed.add_field(name = "Reason:", value = "Ping a role to give {} that role!".format(member.mention))
            embed.set_footer(text = "-_-")
            await ctx.send(embed = embed)
            return
        try:
            addRole = True
            for role_ in member.roles:
                if role_ == role:
                    addRole = False
                    break
            if not addRole:
                embed = discord.Embed(title = ":x: Add Role Failed!", color= ctx.author.color)
                embed.add_field(name = "Reason:", value = "I was unable to add that role to {}!".format(member.mention))
                embed.add_field(name = "Why?",value = f"{member.mention} already has {role.mention}, so...")
                embed.set_footer(text = "-_-")
                await ctx.send(embed = embed)
                return
            else:
                em = discord.Embed(title=  ":white_check_mark: Add Role Successful!", color = ctx.author.color)
                em.add_field(name = "Reason:", value = f"`{reason}`")
                em.add_field(name = "User:", value = f"{member.mention}")
                em.add_field(name = "Role:", value = f"{role.mention}", inline = True)
                em.add_field(name ="Moderator:", value = f"{ctx.author.mention}", inline = False)
                await ctx.send(embed = em)
                return
        except:
            embed = discord.Embed(title = ":x: Addrole Failed!", color= ctx.author.color)
            embed.add_field(name = "Reason:", value = "I was unable to give {} that role!".format(member.mention))
            embed.add_field(name = "Why?",value = "This is usually because of role hierarchy or because I don't have manage roles permissions!")
            embed.set_footer(text = "-_-, gimme the perms m8")
            await ctx.send(embed = embed)
    
    @commands.command(aliases=["takerole", "remover"])
    @has_permissions(manage_roles = True)
    async def removerole(self, ctx, member : discord.Member = None, role : discord.Role = None,*,reason = None):
        if member is None:
            embed = discord.Embed(title = ":x: Removerole Failed!", color= ctx.author.color)
            embed.add_field(name = "Reason:", value = "Ping a user to take away a role from them!")
            embed.set_footer(text = "-_-")
            await ctx.send(embed = embed)
            return
        if role is None:
            embed = discord.Embed(title = ":x: Removerole Failed!", color= ctx.author.color)
            embed.add_field(name = "Reason:", value = "Ping a role to remove that role from {}!".format(member.mention))
            embed.set_footer(text = "-_-")
            await ctx.send(embed = embed)
            return
        try:
            roleRemoved = False
            for role_ in member.roles:
                if role_ == role:
                    await member.remove_roles(role)
                    roleRemoved = True
                    return
            if not roleRemoved:
                embed = discord.Embed(title = "<:x: Remove Role Failed!", color= ctx.author.color)
                embed.add_field(name = "Reason:", value = "I was unable to remove that role from {}!".format(member.mention))
                embed.add_field(name = "Why?",value = f"{member.mention} doesn't even have {role.mention}, so...")
                embed.set_footer(text = "-_-")
                await ctx.send(embed = embed)
                return
            else:
                em = discord.Embed(title=  ":x: Remove Role Successful!", color = ctx.author.color)
                em.add_field(name = "Reason:", value = f"`{reason}`")
                em.add_field(name = "User:", value = f"{member.mention}")
                em.add_field(name = "Role:", value = f"{role.mention}", inline = True)
                em.add_field(name ="Moderator:", value = f"{ctx.author.mention}", inline = False)
                await ctx.send(embed = em)
                return
        except:
            embed = discord.Embed(title = ":x: Remove Role Failed!", color= ctx.author.color)
            embed.add_field(name = "Reason:", value = "I was unable to remove that role from {}!".format(member.mention))
            embed.add_field(name = "Why?",value = "This is usually because of role hierarchy or because I don't have manage roles permissions!")
            embed.set_footer(text = "-_-, gimme the perms dummo")
            await ctx.send(embed = embed)
            return

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title = ":x: Add Role Failed!", color = ctx.author.color)
            em.add_field(name = "Reason:", value = "`Manage Role Permission Missing!`")
            em.set_footer(text = "Imagine thinking you have the perms!")
            await ctx.send(embed = em)
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title = ":x: Add Role Failed!", color = ctx.author.color)
            em.add_field(name = "Reason:", value = "`Ping a user and a role to give the role to the user!`")
            em.set_footer(text = "Addrole properly already!")
            await ctx.send(embed = em)


    @removerole.error
    async def removerole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title = ":x: Remove Role Failed!", color = ctx.author.color)
            em.add_field(name = "Reason:", value = "`Manage Role Permission Missing!`")
            em.set_footer(text = "Imagine thinking you have the perms!")
            await ctx.send(embed = em)
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title = ":x: Remove Role Failed!", color = ctx.author.color)
            em.add_field(name = "Reason:", value = "`Ping a user and a role to remove the role from the user!`")
            em.set_footer(text = "Remove Role properly already!")
            await ctx.send(embed = em)
    #The following two commands belong to BobDotCom on Github. They are NOT MY CODE!!
    @commands.command()
    @commands.has_permissions(ban_members = True)
    @commands.cooldown(1, 1, commands.BucketType.channel)
    async def ban(self, ctx, member: discord.Member, *,reason: str = None):
        """Ban a member with an optional delete_days parameter
        The reason must not start with a number, and you may give a reason without deleting messages"""
        if True:
            try:
                asdf = ctx.author
                f = member.top_role
                h = asdf.top_role
                if h > f or ctx.guild.owner == ctx.author and not member == ctx.author:
                  if member.guild_permissions.ban_members and not ctx.guild.owner == ctx.author:
                    await ctx.send("This person has to not have the ban members permission.")
                  else:
                    await member.ban(delete_message_days=delete_days, reason="Banned by: " + ctx.author.mention + ": " + (reason or "No reason specified"))
                    await ctx.send("Ok, I banned them for you")
                else:
                  if member == ctx.author:
                    await ctx.send("You can't ban yourself. -_-")
                  else:
                    await ctx.send("Error, this person has a higher or equal role to you")
            except:
                await ctx.send(f"Hmmm, I do not have permission to ban {member}, or that is not a valid member")
            try:
                await member.send(f"You have been **banned** from **{ctx.guild}** server due to the following reason:\n**{reason}**")
            except:
                pass

    @commands.command(help="Ban a user by their id.",aliases=['idban'])
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    async def hackban(self, ctx, user_id: int, *, reason: str = None):
        
        member = ctx.guild.get_member(user_id)
        if member:
            ban = self.bot.get_command('ban')
            return await ctx.invoke(ban,member=user_id,reason=reason)
        try:
            class user:
                id = user_id
            await ctx.guild.ban(user,reason=reason)
            await ctx.send("Successfully banned user id **{}** with reason: **{}**. Check the audit logs to make sure I banned the right person.".format(user.id, reason))
        except:
            return await ctx.send("I couldn't do that")

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def announce(ctx, channel : discord.TextChannel, *, msg = None):
        embed = discord.Embed(title = "Announcement!", color = ctx.author.color)
        embed.add_field(name = "Announcement:", value = f"`{msg}`")
        embed.add_field(name = "Moderator:", value = f"`{ctx.author.name}`")
        await channel.send(embed = embed)

    @announce.error
    async def announce_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title = ":x:  Announcement failed!", color = ctx.author.color)
            embed.add_field(name = 'Reason:', value = "Some perms are missing")
            em.set_footer(text = "Imagine thinking you have the perms!")
            await ctx.send(embed = embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title = ":x: Announcement failed!", color = ctx.author.color)
            embed.add_field(name = 'Reason:', value = f"Mention a channel properly! And write a message after it!")
            embed.set_footer(text = 'Do stuff properly!')
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def createrole(self, ctx, *, name = "UnknownRole"):
        role=  await ctx.guild.create_role(name = name)
        em = discord.Embed(title = ":white_check_mark: Role Created", color = ctx.author.color, description = f"{role.mention} was successfully created!")
        em.add_field(name = "Role:", value = f"{role.mention}")
        em.add_field(name ="Moderator:", value = f"{ctx.author.mention}")
        em.set_footer(text = "Good job creating roles!")
        await ctx.send(embed = em)

    @createrole.error
    async def createrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title = ":x: Role Creation Failed")
            em.add_field(name = "Reason:", value = "`Manage Roles perms missing!`")
            em.set_footer(text = "Imagine thinking you have the perms!")
            await ctx.send(embed = em)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod commands Loaded!")

    @commands.command(aliases = ["purge", "massdelete", "bulkdel"])
    @has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 1):
        try:
            amount = int(amount)
        except:
            await ctx.send("Provide an integer amount of messages!")
            return 
        await ctx.channel.purge(limit = amount+1)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title = ":x: Purge Failed!", color = ctx.author.color)
            embed.add_field(name = "Reason:", value = f"`Manage Messages Permissions Missing!`")
            embed.set_footer(text = "Imagine thinking you have the perms!")
            await ctx.send(embed = embed)

    @commands.command()
    @has_permissions(manage_channels = True)
    async def lock(self, ctx, *, reason = None):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        em = discord.Embed(title = f":white_check_mark: Channel has been locked!", color = discord.Color.green())
        em.add_field(name = "**Responsible Moderator:**", value = f"`{ctx.author.name}`")
        em.add_field(name = "**Reason:**", value = f"`{reason}`")
        em.add_field(name=  "Description", value = "You are not muted this channel is locked! No one but mods can type in this channel!", inline = False)
        await ctx.channel.send(embed = em)

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title = ":x: Lock Failed!", color = ctx.author.color)
            embed.add_field(name = "Reason:", value = f"Manage Channels Permissions Missing!")
            embed.set_footer(text = "Imagine thinking you have the perms!")
            await ctx.send(embed = embed)

    @commands.command()
    @has_permissions(manage_channels = True)
    async def unlock(self, ctx, *, reason = None):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
        em = discord.Embed(title = f":white_check_mark: Channel has been unlocked!", color = discord.Color.green())
        em.add_field(name = "**Responsible Moderator:**", value = f"`{ctx.author.name}`")
        em.add_field(name = "**Reason:**", value = f"`{reason}`")
        em.add_field(name=  "Description", value = "You are not unmuted this channel is unlocked! No one but mods can type in this channel!", inline = False)
        await ctx.channel.send(embed = em)

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title = ":x: Unlock Failed!", color = ctx.author.color)
            embed.add_field(name = "Reason:", value = f"Manage Channels Permissions Missing!")
            embed.set_footer(text = "Imagine thinking you have the perms!")
            await ctx.send(embed = embed)

    @commands.command()
    @has_permissions(manage_channels = True)
    async def setdelay(self, ctx, amount = 5, *, reason = None):
        if amount > 6000:
            await ctx.channel.send("Amount needs to be less than 6000!")
            return
        try:
            amount = int(amount)
        except:
            em = discord.Embed(title = ":x: Set Delay Failed", color = ctx.author.color)
            em.add_field(name = "Reason:", value = "Amount is not an integer")
            await ctx.send(embed = em)
            return
        await ctx.channel.edit(slowmode_delay=amount)
        em = discord.Embed(title = ":white_check_mark: Change in channel settings", color = ctx.author.color)
        em.add_field(name = "**Responsible Moderator:**", value = f"`{ctx.author.name}`")
        em.add_field(name = "**Reason:**", value = f"`{reason}`")
        em.add_field(name = "Slowmode", value = f"`{amount} seconds`")
        await ctx.send(embed = em)

    @setdelay.error
    async def setdelay_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title = "Setdelay Failed!", color = ctx.author.color)
            embed.add_field(name = "Reason:", value = f"Manage Channels Permissions Missing!")
            embed.set_footer(text = "Imagine thinking you have the perms!")
            await ctx.send(embed = embed)

    @commands.command(name="unban")
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, username: str = None, *, reason=None):
        if username is None:
            await ctx.send("Insufficient arguments.")
        else:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = username.split('#')

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user,reason="Unbanned by: " + ctx.author.mention + ": " + (reason or "No reason specified"))

            try:
                if reason:
                    await ctx.send(f"User **{username}** has been unbanned for reason: **{reason}**.")
                else:
                    await ctx.send(f"User **{username}** has been unbanned.")
                await user.send(f"You have been **unbanned** from **{ctx.guild}** server due to the following reason:\n**{reason}**")
            except NameError:
                await ctx.send(f"{username} is has not been banned in this server.")

    #normal function
    def convert(self, time):
        pos = ["s","m","h","d"]

        time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2

        return val * time_dict[unit]

    @commands.command()
    @has_permissions(manage_channels = True)
    async def count(self,ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        messages = await channel.history(limit = None).flatten()
        count = len(messages)
        em = discord.Embed(title = f"Count of {channel.mention}", color = ctx.author.color, description = "There are {} messages in {}".format(count, channel.mention))
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Moderation(bot))