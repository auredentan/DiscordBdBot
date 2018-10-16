import discord
from discord.ext import commands
from db.models import Member


class Level:
    def __init__(self, bot, session=None):
        self.bot = bot
        self.session = session

    async def on_message(self, message):
        author = message.author.name
        avatar = message.author.avatar_url
        id = message.author.id

        try:
            count = self.session.query(Member.id).filter(Member.id == id).count()
            if count < 1:
                member = Member(id=id, name=author, avatar=avatar, level = 1, experience = 0)
                self.session.add(member)
            
            await self.add_exp(id)
            await self.level_up(message.author, message.channel)


        except Exception as error:
            await self.bot.say('Could not complete your command')
            print(error)

    async def add_exp(self, user):
        """
            Add experience to a user in the database 

            Args:
                user (object): a discord author
        """
        id = user.id
        try:
            self.session.query(Member).filter(Member.id == id).first().experience += 5            
            self.session.commit()
        except:
            self.session.rollback()
            raise

    async def level_up(self, user, channel):
        """
            Check if the user has leveled up, if so update the database and send a message in the discord chat

            Args:
                user (object): a discord author
                channel (object): a discord channel
        """
        id = user.id
        member = self.session.query(Member).filter(Member.id == id).first()
        exp = member.experience
        current_level = member.level
        next_level = int(exp ** (1/4))


        if current_level < next_level:
            try:
                self.session.query(Member).filter(Member.id == id).first().level += 1                
                self.session.commit()
                await self.bot.send_message(channel, '{} has leveled up to level {}'.format(user.mention, next_level))
            except:
                self.session.rollback()
                raise

def setup(bot, kwargs):
    bot.add_cog(Level(bot, **kwargs))