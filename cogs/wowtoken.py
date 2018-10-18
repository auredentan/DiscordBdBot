import discord
from discord.ext import commands

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests

import datetime
import sqlalchemy
import logging
import os

"""
    Wow api is currently moving to oauth so all the endpoint are not there yet and so 
    this cog is stopped until the api is fully up and running.
"""
class WowToken:
    def __init__(self, bot, session):
        self.bot = bot
        self.session = session
        self.logger = logging.getLogger("DiscordDBBot.WowToken")
        self.client_id = os.getenv('WOW_API_CLIENT_ID')
        self.client_secret = os.getenv('WOW_API_CLIENT_SECRET')

    
    def get_daily_api_token(self):
        client = BackendApplicationClient(client_id = self.client_id)
        oauth = OAuth2Session(client=client)
        token_infos = oauth.fetch_token(
            token_url='https://eu.battle.net/oauth/token', 
            client_id=self.client_id,
            client_secret=self.client_secret)
        return token_infos['access_token']
        
    ## TODO
    def get_wow_token_price(self, token):
        url = 'https://eu.api.blizzard.com/data/wow/token/?access_token={}'.format(token)
        try:
            rep = requests.get(url).json()
        except Exception as error:
            self.logger.error(error)

        if rep['code'] == 200:
            # Request ok => add price in database 
            return rep
        else:
            self.logger.debug("Token api request failed : {}".format(rep))
    
    @commands.command(pass_context=True)
    async def token(self, ctx):
        api_token = self.get_daily_api_token()
        token = self.get_wow_token_price(api_token)
        if token['code'] == 200:
            print(token)
        else:
            await self.bot.say('Something w')
            self.logger.debug(token)

def setup(bot, kwargs):
    bot.add_cog(WowToken(bot, **kwargs))