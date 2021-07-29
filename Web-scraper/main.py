# Swedish News Discord Bot
# By Michal Špano (@michalspano)
# Started 24/07/2021
# Creating a main module (executable)

# Import standard libraries
import os
from discord.ext import commands
from datetime import datetime
from asyncio import sleep as s

# Import core package
from utils.core import WebsiteScraper

# Import HTTPS monitor
from utils.web import keep_alive

# Instantiate a bot client method using Discord commands with a def. prefix '$'
bot = commands.AutoShardedBot(commands.when_mentioned_or("$"), help_command=None)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(aliases=["Start", "start"])
async def start_news_thread(ctx, *, time: int = 10):
    while True:
        # Receive data from web using a web scraper class
        scraped_data_set = WebsiteScraper(path="secrets.json", parser="html5lib").load_website_data()

        # Process scraped data in an embedded message format
        embed_output = WebsiteScraper(path=scraped_data_set).embed_discord_message()

        # Send the embedded message and let the function await in a desire interval
        await ctx.send(embed=embed_output)

        # Delay the post session
        await s(time)


# Instance of the main function
def main():
    keep_alive()
    print(f"Command executed: {datetime.now()}")
    bot.run(os.environ["TOKEN"])


# This is an executable
if __name__ == '__main__':
    # Run the main function
    main()
