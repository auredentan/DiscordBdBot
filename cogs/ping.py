import discord
from discord.ext import commands

class Ping:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        '''Returns pong when called'''
        author = ctx.message.author.name
        server = ctx.message.server.name
        await self.bot.say('Pong for {} from {}!'.format(author, server))

def setup(bot, kwargs):
    bot.add_cog(Ping(bot, **kwargs))