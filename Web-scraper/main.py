# Swedish News Discord Bot
# By Michal Špano (@michalspano)

import discord
import os
from requests_html import HTMLSession
from discord.ext import commands

# Instantiate a bot client method,
# Using default prefix '?'
bot = commands.AutoShardedBot(commands.when_mentioned_or("?"),
                              help_command=None,
                              activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name="Mention me for help."))
# TODO: work on the motivation boost Discord Bot
# TODO: ...


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")

# bot.run(os.environ["TOKEN"])

session = HTMLSession()
url = "https://news.google.com/topstories?hl=sv&gl=SE&ceid=SE:sv"

r = session.get(url)
r.html.render(sleep=1, scrolldown=5)
articles = r.html.find("article")

print(articles)
