# Swedish News Discord Bot
# By Michal Špano (@michalspano)
# Started 24/07/2021

import discord
import os
import json
import requests
import random as r
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from discord.ext import commands
from asyncio import sleep as s

# Instantiate a bot client method,
# Using default prefix '?'
bot = commands.AutoShardedBot(commands.when_mentioned_or("?"), help_command=None,
                              activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name="?start"))


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")


@bot.command(aliases=["Start", "start"])
async def start_news_thread(ctx):
    while True:
        class_instance1 = WebsiteScraper(path="secrets.json", parser="html5lib").load_website_data()
        output = WebsiteScraper(path=class_instance1).embed_discord_message()
        await ctx.send(embed=output)
        await s(30)


# TODO: Create a Website scraper class
class WebsiteScraper:
    def __init__(self, path, parser=None):
        self.path = path
        self.parser = parser

    def load_website_data(self):
        with open(self.path) as secretsJSON:
            secrets = json.load(secretsJSON)

        website_link = secrets["link"]
        web_request = Request(website_link, headers=secrets["headers"])
        web_page = urlopen(web_request).read()

        data_list = []

        # Open a Soup HTML Scraper with requests.Session()
        with requests.Session():
            soup = BeautifulSoup(web_page, self.parser)

            for item in soup.find_all("div", attrs={"class": secrets["article-div"]}):
                raw_link = (item.find("a", href=True))["href"]
                link = raw_link.split("/url?q=")[1].split("&sa=U&")[0]
                title = (item.find("div", attrs={"class": secrets["title-div"]})).get_text()
                data_description = (item.find("div", attrs={"class": secrets["description-div"][0]})).get_text(). \
                    split(secrets["description-div"][1])

                raw_time = str(data_description[0])
                description = data_description[1]

                time_hours = int(raw_time.split()[1])

                time_message = f"{time_hours} hours(s) ago"

                data_set = {"title": title, "description": description,
                            "link": link, "time": time_message}

                data_list.append(data_set)

        return r.choice(data_list)

    def embed_discord_message(self):
        message_data = self.path

        embed_message = discord.Embed(title=message_data["title"], description=message_data["description"],
                                      color=discord.Color.dark_blue())
        embed_message.add_field(name="⌚️  |  Posted", value=message_data["time"], inline=True)

        embed_message.add_field(name="🔗  |  Link", value=f"[Read more here]({message_data['link']})", inline=True)
        embed_message.set_footer(text=f"{bot.user}")

        embed_message.set_thumbnail(url="https://github.com/michalspano/.docs/blob/main/SFU-News.png?raw=true")

        return embed_message


if __name__ == '__main__':
    bot.run(os.environ["TOKEN"])
