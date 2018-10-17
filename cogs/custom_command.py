import discord
from discord.ext import commands
import logging
from db.models import Command


class Custom_Command:
    def __init__(self, bot, session):
        self.bot = bot
        self.session = session
        self.logger = logging.getLogger('DiscordBDBot.custom_command')

    @commands.group(pass_context=True)
    async def custom_command(self, ctx):
        pass

    @custom_command.command(pass_context=True)
    async def help(self, ctx):
        self.logger.info("custom help command")
        clist = [
            'help:\tShow the help\n',
            'add:\tAdd a command\n',
            'update\tUpdate a command',
            'remove:\tRemove a command\n',
            'list:\tList the all the available custom commands\n'
        ]
        help = 'This is the help !\n Here is a list of the basic commands:\n'
        for cmd in clist:
            help += '{}'.format(cmd)
        await self.bot.say(help)

    @custom_command.command(pass_context=True)
    async def add(self, ctx, name, content):
        """
            Add a command (save it bascily)
            The command has a name and a content
        """
        try:
            exist = self.session.query(Command).filter(Command.name == name).count()
            if exist > 0:
                await self.bot.say('The command {} already exist ! You can Remove or update it.'.format(name))
            else:
                cmd = Command(name = name, content = content, description = "")
                self.session.add(cmd)
                self.session.commit()
        except Exception as error:
            await self.bot.say('Could not complete your command')
            self.logger.error(error)

    

def setup(bot, kwargs):
    bot.add_cog(Custom_Command(bot, **kwargs))
