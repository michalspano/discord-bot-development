# Swedish News Discord Bot
# By Michal Špano (@michalspano)
# Started 24/07/2021
# Creating a main module (executable)

# Import standard libraries
import os
import discord
from discord.ext import commands
from datetime import datetime

# Import core package
from utils.core import WebsiteScraper

# Import HTTPS monitor
from utils.web import keep_alive

# Instantiate a bot client method using Discord commands with a def. prefix '$'
bot = commands.AutoShardedBot(commands.when_mentioned_or("$"), help_command=None,
                              activity=discord.Activity(type=discord.ActivityType.listening,
                              name="$news"))


@bot.event
async def on_ready():
    # Determine if bot loaded successfully
    print(f"Logged in as {bot.user}; {datetime.now()}")


@bot.command(aliases=["News", "news", "nw"])
async def start_news_thread(ctx):

    # Receive data from web using a web scraper class
    scraped_data_set = WebsiteScraper(path="secrets.json", parser="html5lib").load_website_data()

    # Process scraped data in an embedded message format
    embed_output = WebsiteScraper(path=scraped_data_set).embed_discord_message()

    # Send the embedded message and let the function await in a desire interval
    await ctx.send(embed=embed_output)


@bot.command(aliases=["Help", "help"])
async def help_command(ctx):

    # Create an instance of a Discord embedded message
    embed_message = discord.Embed(title="Swedish News",
                                  description="A smart web scraper delivering the latest Swedish news 🇸🇪",
                                  colour=discord.Colour.blurple())

    # Add field about the bot commands
    embed_message.add_field(name="👾  |  My commands",
                            value="Use `#News`, `#news`, `#nw`",
                            inline=True)

    # Add field about the developer
    embed_message.add_field(name="👨‍💻  |  Developer",
                            value="[@michalspano](https://github.com/michalspano)",
                            inline=True)

    await ctx.send(embed=embed_message)


# Instance of the main function
def main():
    # keep_alive()
    bot.run(os.environ["TOKEN"])


# This is an executable
if __name__ == '__main__':
    # Run the main function
    main()
