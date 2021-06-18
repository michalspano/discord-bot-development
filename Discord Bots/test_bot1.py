from random import *

import discord
import os
import requests

client = discord.Client()


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

    #  Activity monitor
    print(f"Log -- {user_data}: {user_message} ({message_channel})")

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

        c_count = 0
        for i in range(len(input_message)):
            if input_message[i] == ":":
                c_count += 1
        if c_count == 2:
            user_range = input_message.split(":")
            range_min, range_max = int(user_range[1]), int(user_range[2])
            await message.channel.send(f"Your random number in the range <{range_min}; {range_max}>"
                                       f"\n\n *Result: {randint(range_min, range_max)}*")


quotes = list()
action_count, quote_range = 0, 10
static_path = "https://api.quotable.io/random"
load_random_quotes(static_path, quote_range)
#  bot_token = load_bot_token("bot_token.txt"); deprecated
client.run(os.environ["TOKEN"])
