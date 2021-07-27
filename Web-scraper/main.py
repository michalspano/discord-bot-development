# Swedish News Discord Bot
# By Michal Špano (@michalspano)
# Started 24/07/2021
# Using Slovak web browser settings

# Libraries used
import os
import json
import requests
import discord
import random as r
import logging
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from discord.ext import commands
from asyncio import sleep as s
from web import keep_alive

# Instantiate a bot client method using Discord commands with a def. prefix '?'
bot = commands.AutoShardedBot(commands.when_mentioned_or("?"), help_command=None,
                              activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name="?start"))
# Create a logging instance
logger = logging.getLogger("Discord status LOG")


@bot.event
async def on_ready():
    # Determine when bot is ready
    print(f"Logged in as: {bot.user}")


@bot.command(aliases=["Start", "start"])
async def start_news_thread(ctx, *, time: int = 3600):
    # Function to initialise the news thread
    while True:
        # Receive data from web using a web scraper class
        scraped_data_set = WebsiteScraper(path="secrets.json", parser="html5lib").load_website_data()

        # Process scraped data in an embedded message format
        embed_output = WebsiteScraper(path=scraped_data_set).embed_discord_message()

        # Invoke logger (debugging purposes)
        logger.warning("Sending a new post to the Discord channel...")

        # Send the embedded message and let the function await in a desire interval
        await ctx.send(embed=embed_output)

        # Delay the post submission
        await s(time)


# TODO: Create a Website scraper class
class WebsiteScraper:
    def __init__(self, path, parser=None):
        self.path = path
        self.parser = parser

    def load_website_data(self):
        # Load secrets data from a .json file
        with open(self.path) as secretsJSON:
            secrets = json.load(secretsJSON)

        # Create a web request using the desired link and reade the website
        website_link = secrets["link"]
        web_request = Request(website_link, headers=secrets["headers"])
        web_page = urlopen(web_request).read()

        # Store instances of a web scraper data sets in a list of dicts.
        data_list = list()

        # Open a Soup HTML Scraper with requests.Session()
        with requests.Session():

            # Create an instance of a 'soup' using the BeautifulSoup method
            soup = BeautifulSoup(web_page, self.parser)

            # Iterate through all the 'posts' using a determined class div identifier from the HTMl skeleton
            for item in soup.find_all("div", attrs={"class": secrets["article-div"]}):

                # Get a 'raw' link from the query
                raw_link = (item.find("a", href=True))["href"]

                # Get the link without redundant extensions
                link = raw_link.split("/url?q=")[1].split("&sa=U&")[0]

                # Get the link of the post using a determined class div identifier from the HTMl skeleton
                title = (item.find("div", attrs={"class": secrets["title-div"]})).get_text()

                # Get the description of the post using a determined class div identifier from the HTMl skeleton
                data_description = (item.find("div", attrs={"class": secrets["description-div"][0]})).get_text().\
                    split(secrets["description-div"][1])

                # Split the desc. of the post to time data and the actual description text
                raw_time = str(data_description[0])
                description = data_description[1]

                # Create the final time message (optional)
                # Command out if using an English web browser
                time_message = format_time(raw_time)

                # Create a data set from scraped data
                data_set = {"title": title, "description": description,
                            "link": link, "time": time_message}

                # Append each dict. data set to a global list
                data_list.append(data_set)

        # Return randomly chosen post from the list
        return r.choice(data_list)

    # Embed scraped data in a Discord Embed() message format
    def embed_discord_message(self):
        message_data = self.path

        # Create an instance of a Discord embed message
        embed_message = discord.Embed(title=message_data["title"], description=message_data["description"],
                                      color=discord.Color.dark_blue())

        # Add subfields and populate them with scraped data from the data dict.
        embed_message.add_field(name="⌚️  |  Posted", value=message_data["time"], inline=True)

        embed_message.add_field(name="🔗  |  Link", value=f"[Read more here]({message_data['link']})", inline=True)
        embed_message.set_footer(text=f"{bot.user}")

        # Include the icon of the application as the thumbnail of the embedded message
        embed_message.set_thumbnail(url="https://github.com/michalspano/.docs/blob/main/SFU-News.png?raw=true")
        return embed_message


# Optional function, only when using a non-English web browser (Slovak in this case)
def format_time(raw_t):

    # Detect if hour(s) or min(s)
    def detect_format(a):
        if a == 'h':
            return "hours(s)"
        else:
            return "min(s)"

    # Identifier set as the first char of the string
    identifier = str(raw_t.split()[2])[0]

    # Time key returned from the function
    key = detect_format(identifier)
    time_hours = int(raw_t.split()[1])

    # Return the formatted time message
    return f"{time_hours} {key} ago"


# This is an executable program
if __name__ == '__main__':
    # keep_alive()
    bot.run(os.environ["TOKEN"])
