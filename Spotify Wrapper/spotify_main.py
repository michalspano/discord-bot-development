import random as r
import spotipy
import discord
import os
from spotipy.oauth2 import SpotifyClientCredentials

api = {"discord_client": discord.Client(),
       "spotify_client": spotipy.Spotify(auth_manager=SpotifyClientCredentials())}


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
        embed_title, embed_image, embed_url = data[0], data[1], data[2]
        embed_message = discord.Embed(title=embed_title, url=embed_url)
        embed_message.set_image(url=embed_image)
        return embed_message


@api["discord_client"].event
async def on_ready():  # Log-Status BOT
    print("BOT Status: ON", api["discord_client"].user)


@api["discord_client"].event
async def on_message(message):
    #  Returns None if bot message detected
    if message.author == api["discord_client"].user:
        return

    #  Returns a musical thread, syntax: '!s' - a random song,
    #  '!s/genre' - a random song from a specified genre
    if message.channel.name == "music" and message.content.startswith("!s"):
        if message.content.startswith("!s"):
            msg = message.content.split("/")

            #  If a specific genre is specified
            if len(msg) > 1:
                genre = msg[1]
            else:  # Default genre selection
                genre = r.choice(["Pop", "Hip-Hop", "Rap", "Ambient"])

            #  Randomized arr[song_title, song_cover, song_url]
            final_result = Spotify(artist=f"{genre}").parse_music_data()
            message_object_default_embed = final_result[2]  # Message to embed via in-build Discord Spotify thread
            embed_object = Spotify.embed_music_data(final_result)

            await message.channel.send(embed=embed_object)  # Embed msg
            await message.channel.send(message_object_default_embed)  # Non-embed msg


api["discord_client"].run(os.environ["TOKEN"])
