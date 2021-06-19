from random import *
from datetime import datetime

import discord
import os
import requests
import praw

client = discord.Client()


def load_reddit_api(path):
    with open(path, "r") as redditApi:
        return [str(line.strip()) for line in redditApi]


r_api = load_reddit_api("reddit_data.txt")
reddit = praw.Reddit(client_id=r_api[0],
                     client_secret=r_api[1],
                     user_agent=r_api[2],
                     check_for_async=False)


#  Deprecated functions
# def load_bot_token(path):
#     with open(path, "r") as inputTextFile:
#         return inputTextFile.readline()


# def load_quotes(data_path):
#     with open(data_path, "r") as quotesInputTextFile:
#         return [line.strip() for line in quotesInputTextFile]


def load_random_quotes(api, r):
    global quotes
    quotes.clear()
    for i in range(r):
        random_quote = requests.get(api).json()
        quote_content, quote_author = random_quote["content"], random_quote["author"]
        output_quote = quote_content + "\n\n" + "By: " + quote_author
        quotes.append(output_quote)


def change_range_event(msg, count):
    for i in range(len(msg)):
        if msg[i] == ":":
            count += 1
    if count == 2:
        return True


def load_memes():
    sub_reddit = reddit.subreddit("mathmemes")
    return choice([submission for submission in sub_reddit.top(limit=10)])


@client.event
async def on_ready():
    print(f"Logged in as {client.user} [bot].")


@client.event
async def on_message(message):
    global action_count, quotes
    user_data = str(message.author).split("#")
    user_name, user_code = user_data[0], user_data[1]
    user_message = str(message.content)
    message_channel = str(message.channel.name)
    input_message = user_message.lower()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    #  Activity monitor
    print(f"Log -- {user_data}: {user_message} ({message_channel}) | {current_time}")

    if message.author == client.user:
        return

    #  Greets the user
    if message.channel.name == "general":
        if input_message == "!hi":
            await message.channel.send(f"Hello, {user_name} [#{user_code}]!")

    if action_count >= quote_range:
        print("***Importing new quotes***")
        load_random_quotes(static_path, quote_range)
        action_count = 0

    #  Inputs random motivation quote
    if message.channel.name == "motivation":
        if input_message == "!q":
            action_count += 1
            await message.channel.send(f"Here's a quote just for you: \n"
                                       f"{choice(quotes)}")

    #  Inputs random number
    if message.channel.name == "random":
        if input_message == "!r":
            await message.channel.send(f"Your random number is: *{randint(0, 1000)}*")

        if change_range_event(input_message, 0):
            user_range = input_message.split(":")
            range_min, range_max = int(user_range[1]), int(user_range[2])
            await message.channel.send(f"Your random number in the range <{range_min}; {range_max}>"
                                       f"\n\n *Result: {randint(range_min, range_max)}*")

    if input_message == "!@":
        await message.channel.send("@everyone")

    if input_message == "!i":
        picture_logo = discord.File("/Users/michalspano/Google Drive/Discord Bot Development/Docs/logo_server.png")
        await message.channel.send("This is our logo!", file=picture_logo)

    if input_message == "!i_a":
        animated_logo = discord.File("/Users/michalspano/Google Drive/Discord Bot Development/Docs/sever-animation.gif")
        await message.channel.send("An animated logo!", file=animated_logo)

    if message.channel.name == "memes":
        if input_message == "!m":
            submission_data = load_memes()

            name = submission_data.title
            url = submission_data.url

            em = discord.Embed(title=name)
            em.set_image(url=url)

            await message.channel.send(embed=em)


quotes = list()
action_count, quote_range = 0, 10
static_path = "https://api.quotable.io/random"
load_random_quotes(static_path, quote_range)
#  bot_token = load_bot_token("bot_token.txt"); deprecated
client.run(os.environ["TOKEN"])