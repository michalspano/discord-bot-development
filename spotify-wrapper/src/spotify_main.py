import random as r
import spotipy
import discord
import os
from spotipy.oauth2 import SpotifyClientCredentials
from web import keep_alive

api = {"discord_client": discord.Client(),
       "spotify_client": spotipy.Spotify(auth_manager=SpotifyClientCredentials())}

client = api["discord_client"]


#  Spotify class to parse data from global API via Spotify
class Spotify:
    def __init__(self, artist):
        self.artist = artist

    def parse_music_data(self):
        search_results = api["spotify_client"].search(q=f"{self.artist}", limit=18)
        result_data = [[track["name"], track['album']['images'][0]['url'], track["external_urls"]["spotify"]] for
                       idx, track in enumerate(search_results['tracks']['items'])]
        return r.choice(result_data)

    @staticmethod
    def embed_music_data(data):
        embed_data = {"embed_title": data[0],
                      "embed_image": data[1],
                      "embed_url": data[2]}
        embed_message = discord.Embed(title=embed_data["embed_title"], url=embed_data["embed_url"])
        embed_message.set_image(url=embed_data["embed_image"])
        return embed_message


class HelpCommands:
    def __init__(self, path):
        self.path = path

    #  Returns the !help command content with discord.Embed()
    def embed_help_commands(self):
        help_commands_desc = str()
        with open(self.path, "r") as help_commands:
            for line in help_commands.readlines():
                help_commands_desc += line
        embed_message = discord.Embed(title="?help commands",
                                      description=help_commands_desc,
                                      url=str(os.environ["GITHUB_LINK"]),
                                      color=discord.Color.dark_green())
        embed_message.set_author(name=api["discord_client"].user.display_name,
                                 icon_url=api["discord_client"].user.avatar_url)
        return embed_message


@client.event
async def on_ready():  # Log-Status BOT
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                           name="a song | ?help to start"))  # Custom
    # Bot status
    print("BOT Status: ON", client.user)


@client.event
async def on_message(message):
    #  Returns None if bot message detected
    if message.author == client.user:
        return

    #  Returns a musical thread, syntax: '?s' - a random song,
    #  '?s/genre' - a random song from a specified genre
    if message.content.startswith("?s"):

        msg = message.content.split("/")

        #  If a specific genre is selected
        if len(msg) > 1:
            genre = msg[1]
        else:  # Default genre selection
            genre = r.choice(["Pop", "Hip-Hop", "Rap", "Ambient", "EDM"])

        #  Randomized arr[song_title, song_cover, song_url]
        final_result = Spotify(artist=f"{genre}").parse_music_data()
        message_object_default_embed = final_result[2]  # Message to embed via in-src Discord Spotify thread
        embed_object = Spotify.embed_music_data(final_result)

        await message.channel.send(embed=embed_object)  # Embed msg
        await message.channel.send(message_object_default_embed)  # Non-embed msg / in-built 'Spotify Preview'

    elif message.content.startswith("?help"):
        returned_embed = HelpCommands(path="help_command.txt").embed_help_commands()
        await message.channel.send(embed=returned_embed)


keep_alive()  # Online WebProvider through Flask
client.run(os.environ["TOKEN"])
