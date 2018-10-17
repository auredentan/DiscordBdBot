import discord
from discord.ext import commands
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tabulate import tabulate
import logging

from db.models import Base, Event, Member, Attendance

class EventCmd:
    def __init__(self, bot, session=None):
        self.bot = bot
        self.session = session
        self.logger = logging.getLogger('DiscordBDBot.Event')


    @commands.command(pass_context=True)
    async def create(self, ctx, name: str, date: str, time: str='0:00am'):
        '''Creates an event with specified name and date
            example: ?create party 12/22/2017 1:40pm
        '''
        server = ctx.message.server.name
        date_time = '{} {}'.format(date, time)
        try:
            event_date = datetime.strptime(date_time, '%m/%d/%Y %I:%M%p')
            event = Event(name=name, server=server, date=event_date)
            self.session.add(event)
            self.session.commit()
            await self.bot.say('Event {} created successfully for {}'.format(name, event.date))
        except Exception as e:
            await self.bot.say('Could not complete your command')
            self.logger.error(e)

    @commands.command(pass_context=True)
    async def attend(self, ctx, name: str):
        '''Allows a user to attend an upcoming event
            example: ?attend party
        '''
        author = ctx.message.author.name
        avatar = ctx.message.author.avatar_url
        id = ctx.message.author.id

        try:
            count = self.session.query(Member).filter(Member.id == id).count()
            event = self.session.query(Event).filter(Event.name == name).first()

            # Verify This event exists
            if not event:
                await self.bot.say('This event does not exist')
                return

            # Create member if they do not exist in our database
            if count < 1:
                member = Member(id=id, name=author, avatar=avatar, level = 1, experience = 0)
                self.session.add(member)

            attending = Attendance(member_id=id, event_id=event.id)
            self.session.add(attending)
            self.session.commit()
            await self.bot.say('Member {} is now attending event {}'.format(author, name))
        except Exception as e:
            await self.bot.say('Could not complete your command')
            self.logger.error(e)


    @commands.command()
    async def list(self):
        '''Displays the list of current events
            example: ?list
        '''
        try:
            events = self.session.query(Event).order_by(Event.date).all()
            headers = ['Name', 'Date', 'Server']
            rows = [[e.name, e.date, e.server] for e in events]
            table = tabulate(rows, headers)
            await self.bot.say('```\n' + table + '```')
        except Exception as e:
            await self.bot.say('Could not complete your command')
            self.logger.error(e)


    @commands.command()
    async def view(self, name: str):
        '''Displays information about a specific event
            example: ?view party
        '''
        try:
            event = self.session.query(Event).filter(Event.name == name).first()
            # Verify This event exists
            if not event:
                await self.bot.say('This event does not exist')
                return

            attending = self.session.query(Attendance).filter(Attendance.event_id == event.id).count()
            info = [['Name', event.name], ['Date', event.date], ['Server', event.server], ['Number Attending', attending]]
            await self.bot.say('```\n' + tabulate(info) + '```')
        except Exception as e:
            await self.bot.say('Could not complete your command')
            self.logger.error(e)

def setup(bot, kwargs):
    bot.add_cog(EventCmd(bot, **kwargs))