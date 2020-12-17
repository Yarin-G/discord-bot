import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions, MemberConverter


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['user-info'])
    async def user_info(self, ctx, user: discord.Member):
        """display specific user information"""
        embed = discord.Embed(title="user details:", description=user.mention)
        roles = []
        for role in user.roles:
            if role.name != '@everyone':
                roles.append(role.mention)

        if len(roles) > 0:
            roles = ' , '.join(roles)
        else:
            roles = "user do not have any roles"

        embed.add_field(name="roles:", value=roles)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)


    @has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        """ban specific user from the server"""
        await user.ban(reason=reason)
        await ctx.send(f"**{user.mention} has been banned**")


    @has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        """kick specific user from the server"""
        await user.kick(reason=reason)
        await ctx.send(f"**{user.mention} has been kicked**")


    @has_permissions(administrator=True)
    @commands.command()
    async def mute(self, ctx, user='all'):
        """mute someone/everyone in the voice channel you are connected to"""
        if user == 'all':

            if ctx.author.voice:
                for member in ctx.author.voice.channel.members:
                    await member.edit(mute=True)

                embed = discord.Embed(title=':white_check_mark: Users have been muted :speak_no_evil:  ',
                                      description=f"users in `{ctx.author.voice.channel}` voice channel have been muted")
                await ctx.send(embed=embed)
            else:
                await ctx.send('**:x: you need to be in a voice channel to use this command**')
        else:
            try:
                converter = MemberConverter()
                member = await converter.convert(ctx, user)
                if member.voice:
                    await member.edit(mute=True)
                    await ctx.send("**:white_check_mark: user has been muted**")
                else:
                    await ctx.send("**member is not in a voice channel. can't mute**")
            except:
                await ctx.send(f"""**specify the user you want to mute or type  `all`  to mute everyone 
    in the voice channel you are connected to
    by default all users will be muted**""")


    @has_permissions(administrator=True)
    @commands.command()
    async def unmute(self, ctx, user='all'):
        """unmute someone/everyone in the voice channel you are connected to"""
        if user == 'all':

            if ctx.author.voice:
                for member in ctx.author.voice.channel.members:
                    await member.edit(mute=False)

                embed = discord.Embed(title=':white_check_mark: Users have been unmuted :speaking_head:',
                                      description=f"users in `{ctx.author.voice.channel}` voice channel have been unmuted")
                await ctx.send(embed=embed)
            else:
                await ctx.send('**:x: you need to be in a voice channel to use this command**')
        else:
            try:
                converter = MemberConverter()
                member = await converter.convert(ctx, user)
                if member.voice:
                    await member.edit(mute=True)
                    await ctx.send("**:white_check_mark: user has been unmuted**")
                else:
                    await ctx.send("**member is not in a voice channel. can't unmute**")
            except:
                await ctx.send(f"""**specify the user you want to unmute or type  `all`  to unmute everyone 
        in the voice channel you are connected to
        by default all users will be unmuted**""")


    @has_permissions(administrator=True)
    @commands.command()
    async def deafen(self, ctx, user='all'):
        """deafen someone/everyone in the voice channel you are connected to"""
        if user == 'all':

            if ctx.author.voice:
                for member in ctx.author.voice.channel.members:
                    await member.edit(deafen=True)

                embed = discord.Embed(title=':white_check_mark: Users have been deafened :mute: ',
                                      description=f"users in `{ctx.author.voice.channel}` voice channel have been deafened")
                await ctx.send(embed=embed)
            else:
                await ctx.send('**:x: you need to be in a voice channel to use this command**')
        else:
            try:
                converter = MemberConverter()
                member = await converter.convert(ctx, user)
                if member.voice:
                    await member.edit(deafen=True)
                    await ctx.send("**:white_check_mark: user has been deafened**")
                else:
                    await ctx.send("**member is not in a voice channel. can't deafen**")
            except:
                await ctx.send(f"""**specify the user you want to mute or type  `all`  to deafen everyone 
    in the voice channel you are connected to
    by default all users will be deafened**""")



    @has_permissions(administrator=True)
    @commands.command()
    async def undeafen(self, ctx, user='all'):
        """undeafen someone/everyone in the voice channel you are connected to"""
        if user == 'all':

            if ctx.author.voice:
                for member in ctx.author.voice.channel.members:
                    await member.edit(deafen=False)

                embed = discord.Embed(title=':white_check_mark: Users have been undeafened :speaker: ',
                                      description=f"users in `{ctx.author.voice.channel}` voice channel have been undeafened")
                await ctx.send(embed=embed)
            else:
                await ctx.send('**:x: you need to be in a voice channel to use this command**')
        else:
            try:
                converter = MemberConverter()
                member = await converter.convert(ctx, user)
                if member.voice:
                    await member.edit(deafen=False)
                    await ctx.send("**:white_check_mark: user has been undeafened**")
                else:
                    await ctx.send("**member is not in a voice channel. can't undeafen**")
            except:
                await ctx.send(f"""**specify the user you want to mute or type  `all`  to undeafen everyone 
    in the voice channel you are connected to
    by default all users will be undeafened**""")



    @has_permissions(manage_messages=True)
    @commands.command()
    async def warn(self, ctx, user: discord.Member = None, *, reason=None):
        """warn a specific user in this server"""

        if not reason:
            reason = 'unknown'

        with open('files/warnings.json', 'r') as json_file:  # get json file data
            all_users = json.load(json_file)

        if str(user.id) not in all_users.keys():  # check if this is user's first warning
            all_users[str(user.id)] = [reason]
        else:
            user_warnings = all_users[str(user.id)]
            user_warnings.append(reason)

        with open('files/warnings.json', 'w') as json_file:  # update json file
            json.dump(all_users, json_file)

        embed = discord.Embed(title='User Has Been Warned',
                              description=f'{user.mention} has been warned by {ctx.author.mention}')
        embed.add_field(name='reason:', value=reason)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

        embed = discord.Embed(title='You Have Been Warned', description=f'by {ctx.author.mention}')
        embed.add_field(name='reason:', value=reason)
        embed.set_thumbnail(url=user.avatar_url)
        await user.send(embed=embed)


    @has_permissions(manage_messages=True)
    @commands.command(aliases=['warns'])
    async def warnings(self, ctx, user: discord.Member = None):
        """see specific user warning in this server"""

        with open('files/warnings.json', 'r') as json_file:
            all_users = json.load(json_file)

        embed = None
        if str(user.id) in all_users.keys():  # check if user has warnings in the server
            embed = discord.Embed(title='User warnings', description=f'here are {user.mention} warnings:')
            for i in range(len(all_users[str(user.id)])):
                embed.add_field(name=f'{str(i + 1)})', value=all_users[str(user.id)][i], inline=False)
        else:
            embed = discord.Embed(title="User Don't Have Any Warnings",
                                  description=f"{user.mention} don't have any warnings in this server")

        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)


    @has_permissions(manage_messages=True)
    @commands.command(aliases=['clear_warns', 'clear-warns', 'clear-warnings'])
    async def clear_warnings(self, ctx, user: discord.Member=None):
        """clear specific user warnings in this server"""

        with open('files/warnings.json', 'r') as json_file:
            all_users = json.load(json_file)

        if str(user.id) not in all_users.keys():  # check if user has warnings in the server
            embed = discord.Embed(title="User Don't Have Any Warnings",
                                  description=f"{user.mention} don't have any warnings in this server")
        else:
            all_users.pop(str(user.id))

            with open('files/warnings.json', 'w') as json_file:  # update json file
                json.dump(all_users, json_file)
            embed = discord.Embed(title="User Warnings Have Been Cleaned",
                                  description=f'{user.mention} warnings have been cleaned')

        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(User(bot))
