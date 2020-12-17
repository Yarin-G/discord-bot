import discord
import json
from discord.ext import commands


class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        # ignore if bot joins the server
        if member.bot:
            return

        # send private message to the user
        with open("files/private_welcome_member_message.txt", "r") as welcome_message:
            welcome_message = welcome_message.read()
            humans_member_count = len([m for m in member.guild.members if not m.bot])
            welcome_message = welcome_message.format(user=member.mention, members_count=humans_member_count, server=member.guild.name)

        if welcome_message:  # check if message is not empty
            await member.send(welcome_message)

        # send message to welcomes channel
        with open("files/settings.json", "r") as settings_file:
            settings_file = json.load(settings_file)

            if "welcomes channel" not in settings_file.keys():  # make sure welcomes channel filed exist
                return

            channel = settings_file["welcomes channel"]

            if not channel:  # check if the welcomes chnnel was given or not
                return

            channel = discord.utils.get(member.guild.text_channels, name=channel)

        with open("files/channel_welcome_member_message.txt", "r") as welcome_message:
            welcome_message = welcome_message.read()
            welcome_message = welcome_message.format(user=member.mention, members_count=humans_member_count, server=member.guild.name)

        if welcome_message:  # check if message is not empty
            await channel.send(welcome_message)


def setup(bot):
    bot.add_cog(Greetings(bot))



