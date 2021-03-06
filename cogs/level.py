import discord
from discord.ext import commands
from db.models import Member as DBMember
import logging


from discord.channel import Channel
from discord.ext.commands.bot import Bot
from discord.member import Member
from discord.message import Message
from sqlalchemy.orm.session import Session
from typing import Dict, Optional
class Level:
    def __init__(self, bot: Bot, session: Optional[Session] = None) -> None:
        self.bot = bot
        self.session = session
        self.logger = logging.getLogger('DiscordBDBot.Level')

    async def on_message(self, message: Message) -> None:
        author = message.author.name
        avatar = message.author.avatar_url
        id = message.author.id

        try:
            count = self.session.query(DBMember).filter(DBMember.id == id).count()
            if count < 1:
                member = Member(id=id, name=author, avatar=avatar, level = 1, experience = 0)
                self.session.add(member)
            
            await self.add_exp(id)
            await self.level_up(message.author, message.channel)


        except Exception as error:
            await self.bot.say('Could not complete your command')
            self.logger.error(error)

    async def add_exp(self, id: str) -> None:
        """
            Add experience to a user in the database 

            Args:
                user (object): a discord author
        """
        try:
            self.session.query(DBMember).filter(DBMember.id == id).first().experience += 5            
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            self.logger.error(error)

    async def level_up(self, user: Member, channel: Channel) -> None:
        """
            Check if the user has leveled up, if so update the database and send a message in the discord chat

            Args:
                user (object): a discord author
                channel (object): a discord channel
        """
        id = user.id
        member = self.session.query(DBMember).filter(DBMember.id == id).first()
        exp = member.experience
        current_level = member.level
        next_level = int(exp ** (1/4))


        if current_level < next_level:
            try:
                self.session.query(DBMember).filter(DBMember.id == id).first().level += 1                
                self.session.commit()
                await self.bot.send_message(channel, '{} has leveled up to level {}'.format(user.mention, next_level))
            except Exception as error:
                self.session.rollback()
                self.logger.error(error)

def setup(bot: Bot, kwargs: Dict[str, Session]) -> None:
    bot.add_cog(Level(bot, **kwargs))
