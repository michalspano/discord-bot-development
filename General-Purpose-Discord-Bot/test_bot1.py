from random import *
from datetime import datetime
from keep_alive import keep_alive

import discord
import os
import requests
import praw
import json

client = discord.Client()


def load_reddit_api(path):
    with open(path, "r") as redditApi:
        return [str(line.strip()) for line in redditApi]


r_api = load_reddit_api("reddit_data.txt")
reddit = praw.Reddit(client_id=r_api[0],
                     client_secret=r_api[1],
                     user_agent=r_api[2],
                     check_for_async=False)


def load_random_quotes(api, r):
    global quotes
    quotes.clear()
    for i in range(r):
        random_quote = requests.get(api).json()
        quote_content, quote_author = random_quote["content"], random_quote["author"]
        output_quote = quote_content + "\n\n" + "By: " + quote_author
        quotes.append(output_quote)


def load_inspirational_quotes():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " - " + json_data[0]["a"]
    return quote


def load_encourage_data(path):
    with open(path, "r") as inputEncourageModule:
        loaded_data = [line.strip() for line in inputEncourageModule]
    split_index = loaded_data.index("*")
    return [loaded_data[:split_index], loaded_data[split_index + 1:]]


content = load_encourage_data("notice_me.txt")
emergency_list, encourage_list = content[0], content[1]


#  Syntax: '!m/r/sub' - sub[meme], '!n: x: y'
def check_event(msg, identifier, count):
    for i in range(len(msg)):
        if msg[i] == identifier:
            count += 1
    if count == 2:
        return True


def load_from_custom_reddit(sub, limit):
    sub_reddit = reddit.subreddit(sub)
    return choice([submission for submission in sub_reddit.top(limit=limit)])


def embed_submission(submission):
    sub_name, sub_url = submission.title, submission.url
    embed_message = discord.Embed(title=sub_name)
    embed_message.set_image(url=sub_url)
    return embed_message


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

    if any(word in message.content for word in emergency_list):
        await message.channel.send(f"{choice(encourage_list)} {message.author.mention}")

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

        elif message.content.startswith("!inspire"):
            await message.channel.send(load_inspirational_quotes())

    #  Inputs random number
    if message.channel.name == "random":
        if input_message == "!n":
            await message.channel.send(f"Your random number is: *{randint(0, 1000)}*")

        elif check_event(input_message, ":", 0):
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

    #  Inputs random meme from 'r/mathmemes'
    if message.channel.name == "memes":
        if input_message == "!m":
            subs = ["physicsmemes", "ProgrammerHumor", "mathmemes"]
            submission_data = load_from_custom_reddit(choice(subs), 20)
            await message.channel.send(embed=embed_submission(submission_data))

        elif check_event(input_message, "/", 0):
            subreddit_data = input_message.split("/")[2]
            submission_data = load_from_custom_reddit(subreddit_data, 20)
            await message.channel.send(embed=embed_submission(submission_data))


quotes = list()
action_count, quote_range = 0, 10
static_path = "https://api.quotable.io/random"
load_random_quotes(static_path, quote_range)
#  bot_token = load_bot_token("bot_token.txt"); deprecated
keep_alive()
client.run(os.environ["TOKEN"])
