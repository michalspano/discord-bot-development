# Motivation boost Discord Bot
# By Michal Špano (@michalspano)

import discord
from discord.ext import commands

# Instantiate a bot client method,
# Using default prefix '?'
bot = commands.AutoShardedBot(commands.when_mentioned_or("?"),
                              help_command=None,
                              activity=discord.Activity(type=discord.ActivityType.listening,
                                                        name="Mention me for help."))
# TODO: work on the motivation boost Discord Bot
# TODO: ...
