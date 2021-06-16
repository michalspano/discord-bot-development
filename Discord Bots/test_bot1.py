import discord
from random import *
client = discord.Client()


def load_bot_token(path):
    with open(path, "r") as inputTextFile:
        return inputTextFile.readline()


@client.event
async def detect_bot_status():
    print(f"Logged in as {client.user} [bot].")


@client.event
async def read_message(m):

    if m.author != client.user:
        user_data = str(m.author).split("#")
        user_name, user_code = user_data[0], user_data[1]
        user_message = str(m.content)
        message_channel = str(m.channel.name)

        #  Activity monitor
        print(f"Log -- {user_data}: {user_message} ({message_channel})")

        #  Greets the user
        if m.channel.name == "general":
            if user_message.lower() == "!hi":
                await m.channel.send(f"Hello, {user_name} (#{user_code})!")

        #  Inputs random motivation quote
        if m.channel.name == "motivation":
            if user_message.lower() == "!q":
                await m.channel.send(f"Here's a quote just for you {choice(quotes)}")


quotes = ["“The Best Way To Get Started Is To Quit Talking And Begin Doing.” – Walt Disney",
          "“The Pessimist Sees Difficulty In Every Opportunity. The Optimist Sees Opportunity In Every Difficulty.” – "
          "Winston Churchill",
          "“Don’t Let Yesterday Take Up Too Much Of Today.” – Will Rogers",
          "“We May Encounter Many Defeats But We Must Not Be Defeated.” – Maya Angelou",
          "“Creativity Is Intelligence Having Fun.” – Albert Einstein"]

bot_token = load_bot_token("bot_token.txt")
client.run(bot_token)
