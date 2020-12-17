import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions


class Verify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @has_permissions(administrator=True)
    @commands.command(aliases=['verify-message'])
    async def verify_message(self, ctx):
        """the bot will send a verify message, new users who react to the bot's message will get verified"""
        with open('files/verify_message.txt', 'r') as f:
            msg = await ctx.send(f.read())

        with open("files/verify_info.json", "r") as f:
            verify_info = json.load(f)
            verify_info['verify message id'] = msg.id

        with open("files/verify_info.json", "w") as f:
            json.dump(verify_info, f)

        await msg.add_reaction('✅')


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        if discord.utils.get(user.roles, name="verified"):
            return

        if self.bot.user == user:
            return

        with open("files/verify_info.json", "r") as f:
            msg = json.load(f)

        if 'verify message id' not in msg.keys():
            return

        if payload.message_id != msg['verify message id']:
            return

        msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        author = msg.author
        role = discord.utils.get(author.guild.roles, name='verified')
        try:
            await user.add_roles(role)
            await msg.remove_reaction(payload.emoji, user)
        except discord.DiscordException:
            print("ops, make sure my role is higher than the verified role")


def setup(bot):
    bot.add_cog(Verify(bot))
