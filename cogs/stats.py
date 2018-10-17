import discord
from discord.ext import commands
import logging

class Stats:
    def __init__(self, bot, session):
        self.bot = bot
        self.session = session
        self.logger = logging.getLogger("DiscordBDBot.Stats")

    @commands.command(pass_context=True)
    async def report(self, ctx):
        """Create a status report
        """
        try:
            members = self.bot.get_all_members()
            online, offline, other = 0,0,0
            for member in members:
                if member.status.online:
                    online += 1
                elif member.status.offline:
                    offline += 1
                else:
                    other += 1
            message = discord.Embed(title='Server report',type='rich', colour=discord.Color(0xffb6c1))
            message.add_field(name='Online',value='**{}** online members'.format(online))
            message.add_field(name='Offline',value='**{}** offline members'.format(offline))
            message.add_field(name='Other',value='**{}** other members'.format(other))
            await self.bot.say(embed=message)

        except Exception as error:
            await self.bot.say('The report has failed !')
            self.logger.error(error)

    @commands.command(pass_context=True)
    async def permissions(self, ctx):
        """Show permissions of the mentionned player(s)
        """
        if len(ctx.message.mentions) == 0:
            for perm in ctx.message.author.server_permissions:
                print(perm)
        else:
            users = ctx.message.mentions
            message = discord.Embed(title='Permissions',type='rich', colour=discord.Color(0xffb6c1))
            for user in users:
                t_perm, f_perm = '', ''
                for perm, value in user.server_permissions:
                    if value:
                        t_perm += perm + '\n'
                    else:
                        f_perm += perm + '\n'
                perms = "_**Allowed**_\n" +t_perm + '------\n' + "_**Not allowed**_\n" + f_perm  
                message.add_field(name=user, value='{}'.format(perms))
            await self.bot.say(embed=message)
            

def setup(bot, kwargs):
    bot.add_cog(Stats(bot, **kwargs))