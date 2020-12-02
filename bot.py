import discord
import asyncio
import json
from discord.ext.commands import has_permissions, MemberConverter
from discord.ext import commands

TOKEN = '' # place your bot's token here
PREFIX = '/'
EMBED_COLOR = 0x00ff00 
EMBED_ICON_URL = 'https://i.imgur.com/ZOKp8LH.jpg' # default embed icon
WELCOME_CHANNEL = 'general' # place with welcome text channel


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    print('Bot is up and ready')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{PREFIX}help"))


@bot.event
async def on_guild_join(guild):
    """adds server to warnings.json to specify users' warnings for each server"""
    all_servers = {}

    # add to warnings.json
    with open('warnings.json', 'r') as json_file:  # get json file data
        all_servers = json.load(json_file)

    all_servers[str(guild.id)] = {}
    with open('warnings.json', 'w') as json_file:  # update json file
        json.dump(all_servers, json_file)

    # add to custom_commands.json
    with open('custom_commands.json', 'r') as json_file:  # get json file data
        all_servers = json.load(json_file)

    all_servers[str(guild.id)] = {}
    with open('custom_commands.json', 'w') as json_file:  # update json file
        json.dump(all_servers, json_file)


@bot.event
async def on_guild_remove(guild):
    """removes server from warnings.json"""
    all_servers = {}

    # remove from warnings.json
    with open('warnings.json', 'r') as json_file:  # get json file data
        all_servers = json.load(json_file)
    
    # in case bot was added before he was started
    if str(guild.id) not in all_servers.keys():
        return
    
    all_servers.pop(str(guild.id))
    with open('warnings.json', 'w') as json_file:  # update json file
        json.dump(all_servers, json_file)

    # remove from custom_commands.json
    with open('custom_commands.json', 'r') as json_file:  # get json file data
        all_servers = json.load(json_file)

    all_servers.pop(str(guild.id))
    with open('custom_commands.json', 'w') as json_file:  # update json file
        json.dump(all_servers, json_file)


@bot.event
async def on_member_join(member: discord.Member):
    
    # ignore if this is a bot
    if member.bot:
        return
    
    # send messages to the welcome text channel
    channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL)
    await channel.send(f"{member.mention} joined this server!")
    humans_member_count = len([m for m in member.guild.members if not m.bot])
    await channel.send(f"now in this server there are {humans_member_count} members!")

    # send a message to user
    embed = discord.Embed(title='New Member!', description=f'Hello {member.mention} Welcome to the server!', color=EMBED_COLOR)
    embed.add_field(name='Hello!', value='We hope you will have fun')
    embed.add_field(name=f"to get started, go to the server and type `{PREFIX}server-info`", value=f'you are member number {humans_member_count} in the server!', inline=False)
    embed.set_thumbnail(url=EMBED_ICON_URL)
    await member.send(embed=embed)


@bot.event
async def on_member_remove(member: discord.member):
    
    # ignore if this is a bot
    if member.bot:
        return
    
    channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL)
    await channel.send(f"{member.mention} left this server")

    all_servers = {}
    all_users_warnings = {}
    with open('warnings.json', 'r') as json_file:
        all_servers = json.load(json_file)

    # get all users and their warnings from the server this command was called
    all_users_warnings = all_servers[str(member.guild.id)]
    if str(member.id) in all_users_warnings:  # check if user has warnings in the server
        all_users_warnings.pop(str(member.id))

        with open('warnings.json', 'w') as json_file:  # update json file
            json.dump(all_servers, json_file)


@bot.event
async def on_message(msg: discord.Message=None):
    """use for custom commands"""
    if msg is None or msg.content is None:
        return
    
    if (not msg.content.startswith(PREFIX)) or (len(msg.content) == 1) or (msg.guild is None):
        return
    

    all_servers = {}
    with open('custom_commands.json', 'r') as json_file:  # get json file data
        all_servers = json.load(json_file)
        
    if str(msg.guild.id) not in all_servers.keys():
        print("server not in server list \ntry to remove the bot from the server and add it again")
        return

    current_server_commands = all_servers[str(msg.guild.id)]
    if current_server_commands and (msg.content[1:] in current_server_commands.keys()):
        await msg.channel.send(current_server_commands[msg.content[1:]])
        return

    await bot.process_commands(msg)


@has_permissions(administrator=True)
@bot.command(aliases=['add-command', 'new-command'])
async def add_command(ctx, command_name=None, *command_reply):
    """adds command as command_name. bot will reply with command_reply"""

    if (command_name is None) or (not command_reply):
        await ctx.send(f"use `{PREFIX}help add-command` to see how to use this command")
        return

    try:
        all_servers = {}
        with open('custom_commands.json', 'r') as json_file:  # get json file data
            all_servers = json.load(json_file)
        
        if str(ctx.guild.id) not in all_servers.keys():
            print("server not in server list \ntry to remove the bot from the server and add it again")
            return
    
        current_server = all_servers[str(ctx.guild.id)]
        current_server[command_name] = ' '.join(command_reply)

        with open('custom_commands.json', 'w') as json_file:  # update json file
            json.dump(all_servers, json_file)

        embed = discord.Embed(title="New Command", description=f"`{command_name}` command was added successfully", color=EMBED_COLOR)
        embed.add_field(name='bot will reply with: ', value=f"`{' '.join(command_reply)}`")
        embed.set_thumbnail(url=EMBED_ICON_URL)
        await ctx.send(embed=embed)
    except:
        await ctx.send(f"use `{PREFIX}help add-command` to see how to use this command")


@has_permissions(administrator=True)
@bot.command(aliases=['delete-command', 'del-command'])
async def delete_command(ctx, command_name=None):
    """delete server's custom command"""

    if command_name is None:
        await ctx.send(f"use `{PREFIX}help del-command` to see how to use this command")
        return

    try:
        all_servers = {}
        with open('custom_commands.json', 'r') as json_file:  # get json file data
            all_servers = json.load(json_file)
        
        if str(ctx.guild.id) not in all_servers.keys():
            print("server not in server list \ntry to remove the bot from the server and add it again")
            return
                        
        current_server = all_servers[str(ctx.guild.id)]
        if command_name in current_server.keys():
            current_server.pop(command_name)
            with open('custom_commands.json', 'w') as json_file:  # update json file
                json.dump(all_servers, json_file)

            await ctx.send(f'**:thumbsup: `{command_name}` custom command has been deleted successfully!**')
        else:
            await ctx.send(f"there is no `{command_name}` custom command.")
    except:
        await ctx.send(f"use `{PREFIX}help del-command` to see how to use this command")


@bot.command(aliases=['custom-commands'])
async def custom_commands(ctx):
    """display server's custom commands"""

    all_servers = {}
    with open('custom_commands.json', 'r') as json_file:  # get json file data
        all_servers = json.load(json_file)

    current_server = all_servers[str(ctx.guild.id)]
                        
    if str(ctx.guild.id) not in all_servers.keys():
        print("server not in server list \ntry to remove the bot from the server and add it again")
        return
                        
    if current_server:
        embed = discord.Embed(title="Server Custom Commands", description="here are the server's custom commands: ", color=EMBED_COLOR)
        for command in current_server.keys():
            embed.add_field(name=command, value=current_server[command], inline=False)
    else:
        embed = discord.Embed(title="Server Does Not Have Custom Commands", description=f"this server doesn't have any custom commands. type `{PREFIX}add-command` to add first command", color=EMBED_COLOR)

    embed.set_thumbnail(url=EMBED_ICON_URL)
    await ctx.send(embed=embed)


@bot.command(aliases=['PING', 'Ping'])
async def ping(ctx):
    """bot response time"""
    await ctx.send(f'**:ping_pong: Pong! \ntime: {round(bot.latency * 1000)}ms**')


@bot.command(aliases=['server-info', 'server-information'])
async def server_info(ctx):
    """display information about the server"""
    embed = discord.Embed(title='Server Info', description='here is the server information:', color=EMBED_COLOR)
    humans_member_count = len([m for m in ctx.guild.members if not m.bot])
    bots_count = len(ctx.guild.members) - humans_member_count
    embed.add_field(name='members:', value=humans_member_count)
    embed.add_field(name='bots:', value=bots_count)
    embed.set_thumbnail(url=EMBED_ICON_URL)
    await ctx.send(embed=embed)


@bot.command(aliases=['role-info', 'role-information'])
async def role_info(ctx, role: discord.Role=None):
    """display information about specific role in the server"""
    if role is None:
        await ctx.send(f"use `{PREFIX}help role_info` to see how to use this command")
        return

    embed = discord.Embed(title=f'{role} Info', description=f'here is information about: {role}', color=EMBED_COLOR)
    embed.add_field(name='permissions:', value=role.permissions.value)
    embed.set_thumbnail(url=EMBED_ICON_URL)
    await ctx.send(embed=embed)


@bot.command()
async def timer(ctx, time=None):
    """set a timer
    time should be in this format (X = number):
        timer Xh - sets a timer for X hours
        timer Xm - sets a timer for X minutes
        timer Xs / X - Xh - sets a timer for X seconds
    """

    if not time:
        await ctx.send(f"use `{PREFIX}help timer` to see how to use this command")
        return

    if '.' not in time:
        time_in_sec = 0
        if (time[-1] == 'h') and (time.count('h') == 1):
            time_in_sec = int(time[:-1]) * 3600
        elif (time[-1] == 'm') and (time.count('m') == 1):
            time_in_sec = int(time[:-1]) * 60
        elif (time[-1] == 's') and (time.count('s') == 1):
            time_in_sec = int(time[:-1])
        elif time.isdigit():
            time_in_sec = int(time)
        else:
            await ctx.send(f"use `{PREFIX}help timer` to see how to use this command")
            return

        await ctx.send(f'**:thumbsup: timer for `{time}` by {ctx.author.mention} has been set!**')
        await asyncio.sleep(time_in_sec)
        await ctx.send(f'**:timer: timer for `{time}` by {ctx.author.mention} is over!**')
    else:
        await ctx.send('**insert only integer type for timer**')


@bot.command()
async def invite(ctx):
    """generate an invite link to this server"""
    invite_link = await ctx.channel.create_invite()
    embed = discord.Embed(title='Server invite', description='send this link to invite people to this server', color=EMBED_COLOR)
    embed.add_field(name='link:', value=invite_link, inline=False)
    embed.set_thumbnail(url=EMBED_ICON_URL)
    await ctx.send(embed=embed)


@bot.command()
@has_permissions(administrator=True)
async def mute(ctx, user='all'):
    """server mute everyone in the voice channel you are connected to, or specific user
    note - by default bot will mute everyone on your voice channel when no user given"""

    if user == 'all':

        if ctx.author.voice:
            for member in ctx.author.voice.channel.members:
                await member.edit(mute=True)

            embed = discord.Embed(title='Users have been muted :mute: ', description=f"users in `{ctx.author.voice.channel}` voice channel have been muted", color=EMBED_COLOR)
            embed.set_thumbnail(url=EMBED_ICON_URL)
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
            await ctx.send(f"use `{PREFIX}help mute` to see how to use this command")


@bot.command()
@has_permissions(administrator=True)
async def unmute(ctx, user='all'):
    """server unmute everyone in the voice channel you are connected to, or specific user
    note - by default bot will unmute everyone on your voice channel when no user given"""

    if user == 'all':
        if ctx.author.voice:
            for member in ctx.author.voice.channel.members:
                await member.edit(mute=False)

            embed = discord.Embed(title='Users have been unmuted :microphone2:', description=f"users in `{ctx.author.voice.channel}` voice channel have been unmuted", color=EMBED_COLOR)
            embed.set_thumbnail(url=EMBED_ICON_URL)
            await ctx.send(embed=embed)
        else:
            await ctx.send('**:x: you need to be in a voice channel to use this command**')
    else:
        try:
            converter = MemberConverter()
            member = await converter.convert(ctx, user)
            if member.voice:
                await member.edit(mute=False)
                await ctx.send("**:white_check_mark: user has been unmuted**")
            else:
                await ctx.send("**member is not in a voice channel. can't unmute**")
        except:
            await ctx.send(f"use `{PREFIX}help unmute` to see how to use this command")


@has_permissions(manage_messages=True)
@bot.command()
async def clear(ctx, amount=1):
    """clear X messages
    note- by default amount=1"""
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'**:wastebasket: {amount} messages have been deleted!**')
    await asyncio.sleep(5)
    await ctx.channel.purge(limit=1)


@bot.command()
@has_permissions(kick_members=True, ban_members=True)
async def info(ctx, member: discord.Member=None):
    """display information about a user"""
    if member is None:
        await ctx.send(f"use `{PREFIX}help info` to see how to use this command")
        return

    roles = []
    for role in member.roles:
        if role != '@everyone':
            roles.append(role.mention)

    embed = discord.Embed(title=f'{member} Info:', description='user roles', color=EMBED_COLOR)
    embed.add_field(name='top role:', value=member.top_role)
    embed.add_field(name='roles:', value=', '.join(roles))
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
@has_permissions(kick_members=True, ban_members=True)
async def kick(ctx, member: discord.Member=None, *, reason=None):
    """kick a user from this server"""
    if member is None:
        await ctx.send(f"use `{PREFIX}help kick` to see how to use this command")
        return

    await member.kick(reason=reason)
    embed = discord.Embed(title=f'{member} has been kicked', description=f"reason: {'unknown' if not reason else reason}", color=EMBED_COLOR)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None, *, reason=None):
    """ban a user from this server"""
    if member is None:
        await ctx.send(f"use `{PREFIX}help ban` to see how to use this command")
        return

    await member.ban(reason=reason)
    embed = discord.Embed(title=f'{member} has been banned', description=f"reason: {'unknown' if not reason else reason}", color=EMBED_COLOR)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)


@has_permissions(manage_channels=True)
@bot.command()
async def warn(ctx, member: discord.Member=None, *reason):
    """warn a specific user in this server"""
    all_servers = {}
    all_users_warnings = {}

    if member is None:
        await ctx.send(f"use `{PREFIX}help warn` to see how to use this command")
        return

    if not reason:
        reason = 'unknown'
    else:
        reason = ' '.join(reason)

    with open('warnings.json', 'r') as json_file:  # get json file data
        all_servers = json.load(json_file)

    if str(ctx.guild.id) not in all_servers.keys():
        print("server not in server list \ntry to remove the bot from the server and add it again")
        return

    all_users_warnings = all_servers[str(ctx.guild.id)]  # get all users and their warnings from the server this command was called
    if str(member.id) not in all_users_warnings.keys():  # check if this is user's first warning
        all_users_warnings[str(member.id)] = [reason]
    else:
        user_warnings = all_users_warnings[str(member.id)]
        user_warnings.append(reason)

    with open('warnings.json', 'w') as json_file:  # update json file
        json.dump(all_servers, json_file)

    embed = discord.Embed(title='User Has Been Warned', description=f'{member.mention} has been warned by {ctx.author.mention}', color=EMBED_COLOR)
    embed.add_field(name='reason:', value=reason)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)

    embed = discord.Embed(title='You Have Been Warned', description=f'by {ctx.author.mention}', color=EMBED_COLOR)
    embed.add_field(name='reason:', value=reason)
    embed.set_thumbnail(url=member.avatar_url)
    await member.send(embed=embed)


@bot.command(aliases=['warns'])
async def warnings(ctx, member: discord.Member=None):
    """see specific user warning in this server"""
    if member is None:
        await ctx.send(f"use `{PREFIX}help warnings` to see how to use this command")
        return

    all_servers = {}
    all_users_warnings = {}
    with open('warnings.json', 'r') as json_file:
        all_servers = json.load(json_file)

    # get all users and their warnings from the server this command was called
    if str(ctx.guild.id) not in all_servers.keys():
        print("server not in server list \ntry to remove the bot from the server and add it again")
        return

    all_users_warnings = all_servers[str(ctx.guild.id)]
    embed = None
    if str(member.id) in all_users_warnings:  # check if user has warnings in the server
        embed = discord.Embed(title='User warnings', description=f'here are {member.mention} warnings:', color=EMBED_COLOR)
        for i in range(len(all_users_warnings[str(member.id)])):
            embed.add_field(name=f'{str(i + 1)})', value=all_users_warnings[str(member.id)][i], inline=False)
    else:
        embed = discord.Embed(title="User Don't Have Any Warnings", description=f"{member.mention} don't have any warnings in this server", color=EMBED_COLOR)

    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)


@has_permissions(manage_channels=True)
@bot.command(aliases=['clear_warns', 'clear-warns', 'clear-warnings'])
async def clear_warnings(ctx, member: discord.Member=None):
    """clear specific user warnings in this server"""
    if member is None:
        await ctx.send(f"use `{PREFIX}help clear_warnings` to see how to use this command")
        return

    all_servers = {}
    all_users_warnings = {}
    with open('warnings.json', 'r') as json_file:
        all_servers = json.load(json_file)

    # get all users and their warnings from the server this command was called
    if str(ctx.guild.id) not in all_servers.keys():
        print("server not in server list \ntry to remove the bot from the server and add it again")
        return

    all_users_warnings = all_servers[str(ctx.guild.id)]
    if str(member.id) not in all_users_warnings:  # check if user has warnings in the server
        embed = discord.Embed(title="User Don't Have Any Warnings", description=f"{member.mention} don't have any warnings in this server", color=EMBED_COLOR)
    else:
        all_users_warnings.pop(str(member.id))

        with open('warnings.json', 'w') as json_file:  # update json file
            json.dump(all_servers, json_file)
        embed = discord.Embed(title="User Warnings Have Been Cleaned", description=f'{member.mention} warnings have been cleaned', color=EMBED_COLOR)

    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)



@bot.event
async def on_command_error(ctx, error):
    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**:x: You don't have the required permission to use this command**")
                          
    if isinstance(error, commands.CommandNotFound):
        pass

                          
bot.run(TOKEN)
