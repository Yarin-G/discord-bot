import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions


class CustomCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, msg):

        with open('files/custom_commands.json', 'r') as json_file:  # get json file data
            all_commands = json.load(json_file)

        if all_commands and (msg.content[1:] in all_commands.keys()):
            await msg.channel.send(all_commands[msg.content[1:]])
            return


    @has_permissions(administrator=True)
    @commands.command(aliases=['add-command', 'new-command'])
    async def add_command(self, ctx, command_name, *, command_reply):
        """add custom commands"""
        if (command_name is None) or (not command_reply):
            return

        with open('files/custom_commands.json', 'r') as json_file:  # get json file data
            all_commands = json.load(json_file)

        all_commands[command_name] = command_reply

        with open('files/custom_commands.json', 'w') as json_file:  # update json file
            json.dump(all_commands, json_file)

        embed = discord.Embed(title="New Command", description=f"`{command_name}` command was added successfully",)
        embed.add_field(name='bot will reply with: ', value=f"`{command_reply}`")
        await ctx.send(embed=embed)


    @has_permissions(administrator=True)
    @commands.command(aliases=['delete-command', 'del-command'])
    async def delete_command(self, ctx, command_name):
        """delete server's custom command"""

        with open('files/custom_commands.json', 'r') as json_file:  # get json file data
            all_commands = json.load(json_file)

        if command_name not in all_commands.keys():
            await ctx.send(f"**there is no `{command_name}` custom command.**")
            return

        all_commands.pop(command_name)
        with open('files/custom_commands.json', 'w') as json_file:  # update json file
            json.dump(all_commands, json_file)

        await ctx.send(f'**:thumbsup: `{command_name}` custom command has been deleted successfully!**')



    @commands.command(aliases=['custom-commands'])
    async def custom_commands(self, ctx):
        """display server's custom commands"""

        with open('files/custom_commands.json', 'r') as json_file:  # get json file data
            all_servers = json.load(json_file)


        if all_servers:
            embed = discord.Embed(title="Server Custom Commands", description="here are the server's custom commands: ")
            for command in all_servers.keys():
                embed.add_field(name=command, value=all_servers[command], inline=False)
        else:
            embed = discord.Embed(title="Server Does Not Have Custom Commands",
                                  description=f"this server doesn't have any custom commands. type `add-command` to add first command")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CustomCommands(bot))



