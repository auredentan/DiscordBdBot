from os import getenv
import discord
from discord.ext import commands
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import importlib


from db.models import Base, Event, Member, Attendance

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


cogs = [
    ('ping', {}),
    ('event', {'session': session}),
    ('level', {'session': session})
    ]

if __name__ == '__main__':
    for cog, kwargs in cogs:
        try:
            lib = importlib.import_module("cogs." + cog)
            lib.setup(bot, kwargs)
            print("{} has been setup correctly !".format(cog))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(cog, error))
    
    try:
        bot.run(token)
    except Exception as e:
        print('Could Not Start Bot')
        print(e)
    finally:
        print('Closing Session')
        session.close()