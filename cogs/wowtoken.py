import discord
from discord.ext import commands

from requests_oauthlib import OAuth2Session
import requests

import plotly.plotly as py
import plotly.graph_objs as go
import plotly

from db.models import Token

import asyncio
import datetime
import sqlalchemy
import logging
import os

PLOTLY_USERNAME = os.getenv('PLOTLY_USERNAME')
PLOTLY_API_KEY = os.getenv('PLOTLY_API_KEY')
plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)


OAUTH2_CLIENT_ID = os.getenv('WOW_API_CLIENT_ID')
OAUTH2_CLIENT_SECRET = os.getenv('WOW_API_CLIENT_SECRET')
class WowToken:
    def __init__(self, bot, session):
        self.bot = bot
        self.session = session
        self.logger = logging.getLogger("DiscordBDBot.WowToken")

    
    def get_daily_api_token(self):
        url = "https://eu.battle.net/oauth/token?grant_type=client_credentials&client_id={}&client_secret={}".format(OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET)
        tok = requests.get(url).json()['access_token']
        return tok
        

    def get_wow_token_price(self, token):
        url = 'https://eu.api.blizzard.com/data/wow/token/?namespace=dynamic-eu&locale=fr_FR&access_token={}'.format(token)
        rep = requests.get(url).json()
        return rep
    
    async def add_or_not(self, date, price):
        """
            Add or not the token price the database
        """
        count = self.session.query(Token).filter(Token.date == date).count()
        if count < 1:
            token = Token(date= date, price = price)
            self.session.add(token)  

    async def background_token_price(self):
        try:
            api_token = self.get_daily_api_token()
            token_infos = self.get_wow_token_price(api_token)

            price = token_infos['price']
            date = datetime.datetime.fromtimestamp(float(str(token_infos['last_updated_timestamp'])[:10]))
            await self.add_or_not(date, price)
            await asyncio.sleep(3600*6)
        except Exception as error:
            print(error)
            self.logger.error(error)
    
    """
        ?token command
    """
    async def construct_graph(self):
        """
            Construct a graph of the token price evolution
        """
        count = self.session.query(Token).count()
        link = None
        if count > 5:
            dates = [date for date in self.session.query(Token.date).distinct()]
            prices = [float(str(price[0])[:-4]) for price in self.session.query(Token.price).distinct()]

            data = [go.Scatter(x=dates, y=prices)]
            link = py.plot(data, filename = 'basic-line', auto_open=False)
        return link

    @commands.command(pass_context=True)
    async def token(self, ctx):
        try:
            api_token = self.get_daily_api_token()
            token_infos = self.get_wow_token_price(api_token)

            price = token_infos['price']
            date = datetime.datetime.fromtimestamp(float(str(token_infos['last_updated_timestamp'])[:10]))
            await self.add_or_not(date, price)
            link = await self.construct_graph()

            message = discord.Embed(title='Wow Token price report',type='rich', colour=discord.Color(0xffb6c1))
            message.add_field(name='Current token price', value='Price = {} golds'.format(float(str(price)[:-4])))
            if link:
                message.add_field(name='Graph link',value='{}'.format(link), inline=False)
            await self.bot.say(embed=message)

        except Exception as error:
            await self.bot.say('Something went wrong !')
            self.logger.error(error)
        
    async def on_ready(self):
        self.bot.loop.create_task(self.background_token_price())
        

def setup(bot, kwargs):
    bot.add_cog(WowToken(bot, **kwargs))