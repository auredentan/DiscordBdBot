A Discord bot with database and cogs
====================================

This is a simple discord bot with an event and a level cog (extension).

It uses ``sqlalchemy`` to handle the database.

**Setup**
=========

`Python version: 3.6`

**_Localy_**
```sh
git clone https://github.com/auredentan/DiscordWithDbBot.git
cd DiscordWithDbBot
export BOT_TOKEN="your_bot_token" 
pip install -r requirements.txt
python bot.py
```

**_Deployment with [heroku](https://www.heroku.com/)_**

```sh
git clone https://github.com/auredentan/DiscordWithDbBot.git
cd DiscordWithDbBot
heroku login
heroku create
heroku config:set BOT_TOKEN="your_bot_token"
git add .
git commit -m "Whatever"
git push heroku master
heroku ps:scale worker=1
```

You can also add the token, launch and monitor your app via their website.
