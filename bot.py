from os import getenv
import discord
from discord.ext import commands
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import importlib

from db.models import Base, Event, Member, Attendance

import logging

logger = logging.getLogger('DiscordBDBot')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

engine = create_engine('sqlite:///event-bot.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


# If table doesn't exist, Create the database
if not engine.dialect.has_table(engine, 'event'):
    Base.metadata.create_all(engine)

description = 'A nice little event bot'
bot = commands.Bot(command_prefix='?', description=description)
token = getenv('BOT_TOKEN')

@bot.event
async def on_ready():
    print(bot.user.id)
    print(bot.user.name)
    print('---------------')
    print('This bot is ready for action!')

helper = {}
cogs = [
    ('ping', {}),
    ('event', {'session': session}),
    ('level', {'session': session}),
    ('stats', {'session': session}),
    ('music', {}),
    ('wowtoken', {'session': session})
    ]

if __name__ == '__main__':
    for cog, kwargs in cogs:
        try:
            lib = importlib.import_module("cogs." + cog)
            lib.setup(bot, kwargs)
            print("{} has been setup correctly !".format(cog))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(cog, error))
            logger.error(error)
    
    try:
        bot.run(token)
    except Exception as error:
        print('Could Not Start Bot')
        logger.error(error)
    finally:
        print('Closing Session')
        session.close()