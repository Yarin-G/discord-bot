import discord
import asyncio
import time
from discord.ext import commands
from datetime import datetime


class Clock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def timer(self, ctx, time):
        """set a timer in this format [time]s/m/h
        h - hours
        m - minutes
        s - seconds"""

        if not time[:-1].isdigit():  # make sure to specify time
            return

        time_in_sec = await convert_time_to_seconds(time)

        if time_in_sec == 0:  # make sure to specify time
            return

        units = await convert_time_to_words(time)
        await ctx.send(f"**:thumbsup: timer for {time[:-1]} {units} by {ctx.message.author.mention} has been set :timer:**")
        await asyncio.sleep(time_in_sec)
        await ctx.send(f"**timer for {time[:-1]} {units} by {ctx.message.author.mention} is up!**", tts=True)


    @commands.command()
    async def remind(self, ctx, channel_or_user: discord.TextChannel, time, *, text):
        """send a message to a text channel after some time.
        use this format [time]s/m/h
        h - hours
        m - minutes
        s - seconds
        """

        if not time[:-1].isdigit():  # make sure to specify time
            return

        time_in_sec = await convert_time_to_seconds(time)

        if time_in_sec == 0:  # make sure to specify time
            return

        units = await convert_time_to_words(time)
        await ctx.send(f"**:thumbsup: remainder for {time[:-1]} {units}  has been set to {channel_or_user.mention} by {ctx.message.author.mention}**")
        await asyncio.sleep(time_in_sec)
        await channel_or_user.send(text)


    @commands.command()
    async def time(self, ctx):
        """display current time"""
        time = datetime.now().strftime("%H:%M")
        await ctx.send(f"**current time is {time}**")


def setup(bot):
    bot.add_cog(Clock(bot))


async def convert_time_to_seconds(time):

    time_in_sec = 0
    if (time[-1] == 'h') and (time.count('h') == 1):
        time_in_sec = int(time[:-1]) * 3600
    elif (time[-1] == 'm') and (time.count('m') == 1):
        time_in_sec = int(time[:-1]) * 60
    elif (time[-1] == 's') and (time.count('s') == 1):
        time_in_sec = int(time[:-1])

    return time_in_sec


async def convert_time_to_words(time):

    if (time[-1] == 'h') and (time.count('h') == 1):
        return "hours"
    elif (time[-1] == 'm') and (time.count('m') == 1):
        return "minutes"
    elif (time[-1] == 's') and (time.count('s') == 1):
        return "seconds"

    return None
