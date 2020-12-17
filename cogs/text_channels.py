import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions


class TextChannels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_messages=True)
    @commands.command()
    async def clear(self, ctx, number_of_messages=10):
        """delete messages in this channel"""
        await ctx.channel.purge(limit=number_of_messages)
        await ctx.send(f'**:thumbsup: {number_of_messages} messages have been deleted! :wastebasket:**', delete_after=5.0)



    @has_permissions(manage_messages=True)
    @commands.command(aliases=['slow-mode'])
    async def slow_mode(self, ctx, delay=0):
        """enable/disable slow mode"""
        await ctx.channel.edit(slowmode_delay=delay)
        await ctx.send(f"**:thumbsup: Set the slowmode delay in this channel to {delay} seconds!**")


def setup(bot):
    bot.add_cog(TextChannels(bot))



