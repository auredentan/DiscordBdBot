A Discord bot with database and cogs
====================================

This is a simple discord bot with some cogs.

The cogs are:
* ``Level``: A level system.
* ``Event``: A basic event system.
* ``Music``: A music part that search and plays music on youtube.
* ``Stats``: A little stat system.
* ``Wowtoken``: A basic sytem that allow you to get the current wow token price .

It uses ``sqlalchemy`` to handle the database.

**Environement variables**
==========================
In order for the bot or some cogs to work you need to setup environnement variables (or replace in code directly)

**Main bot**
------------

To launch the bot you need to have a token corresponding to your bot (you can get it on your discord bot page)

```sh
export BOT_TOKEN=<your_bot_token>
```

**Wowtoken cog**
----------------

It need your blizzard api infos in order to make api calls.

```sh
export WOW_API_CLIENT_ID=<your_blizzard_api_client_id>
export WOW_API_CLIENT_SECRET=<your_blizzard_api_secret>
```
_Optionnal_

Also this cog use Plotly to generate graphs.
```sh
export PLOTLY_USERNAME=<your_plotly_username>
export PLOTLY_API_KEY=<your_plotly_api_key>
```

**Setup**
=========

`Python version: 3.6`

**_Localy_**
```sh
git clone https://github.com/auredentan/DiscordBdBot.git
cd DiscordBdBot
export BOT_TOKEN="your_bot_token" 
pip install -r requirements.txt
python bot.py

# website
gunicorn website.app:app
```

**_Deployment with [heroku](https://www.heroku.com/)_**

```sh
git clone https://github.com/auredentan/DiscordBdBot.git
cd DiscordBdBot
heroku login
heroku create
heroku config:set BOT_TOKEN="your_bot_token"
git add .
git commit -m "Whatever"
git push heroku master
heroku ps:scale bot=1

# website
heroku ps:scale web=1
```

You can also add the token, launch and monitor your app via their website.
