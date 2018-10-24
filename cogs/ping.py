import discord
from discord.ext import commands

from discord.ext.commands.bot import Bot
from typing import Any, Dict
class Ping:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        '''Returns pong when called'''
        author = ctx.message.author.name
        server = ctx.message.server.name
        await self.bot.say('Pong for {} from {}!'.format(author, server))

def setup(bot: Bot, kwargs: Dict[Any, Any]) -> None:
    bot.add_cog(Ping(bot, **kwargs))
