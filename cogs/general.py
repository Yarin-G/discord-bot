import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """bot response time"""
        msg = await ctx.send(f"**pinging...**")
        await msg.edit(content=f"**:stopwatch:  _{round(self.bot.latency * 1000)}_ ms**")


    @has_permissions(administrator=True)
    @commands.command()
    async def shutdown(self, ctx):
        """shut the bot down"""
        await ctx.send("shutting down...")
        try:
            await self.bot.logout()
        except:
            await ctx.send("EnvironmentError")
            self.bot.clear()


    @commands.command()
    async def invite(self, ctx):
        """generate an invite link to this server"""
        invite_link = await ctx.channel.create_invite()
        embed = discord.Embed(title='Server invite', description='send this link to invite people to this server')
        embed.add_field(name='link:', value=invite_link, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
