import os
from dotenv import load_dotenv
import asyncio
import json

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

import logging

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
intents.voice_states = True

bot = commands.Bot(intents=intents, command_prefix='!')

bot.global_config = {}

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='commands.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.before_invoke
async def on_command(ctx):
    logger.info(f'Command received: {ctx.message.content} Member ID: {ctx.author.id} Member Name: {ctx.author.display_name} Channel: {ctx.channel.name}')

async def send_error_message(bot, error, context="General"):
    cog_name = "Unknown"
    class_name = "Unknown"
    context_info = "Unknown"

    if hasattr(context, "__class__"):
        class_name = context.__class__.__name__
        if hasattr(context, "cog") and context.cog:
            cog_name = context.cog.qualified_name

    if isinstance(context, commands.Context):
        context_info = f"Command: {context.command} by {context.author} in #{context.channel.name}"

    error_message = (
        f"Error in Cog: {cog_name} - Class: {class_name}\n"
        f"Context: {context_info}\n"
        f"Details: {error}"
    )

    bot_channel = bot.get_channel(bot.global_config['bot_channel'])
    if bot_channel:
        await bot_channel.send(error_message)
    else:
        print(error_message)

bot.send_error_message = lambda error, context="General": send_error_message(bot, error, context)

def load_config():
    try:
        with open("config.json", "r") as f:
            bot.global_config = json.load(f)

        if "bot_channel" not in bot.global_config:
            print("Error: The configuration file is missing the 'bot_channel' key. Please add it to config.json.")
            exit(1)

        bot_channel_id = bot.global_config["bot_channel"]
        if not isinstance(bot_channel_id, int):
            print("Error: The 'bot_channel' value in config.json must be a valid integer representing the channel ID.")
            exit(1)

    except json.JSONDecodeError:
        print("Error: The configuration file (config.json) is not a valid JSON. Please fix it.")
        exit(1)
    except FileNotFoundError:
        print("Error: The configuration file (config.json) is missing. Please create it.")
        exit(1)

@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: {bot.command_prefix}\n-----")
    bot_channel_id = bot.global_config["bot_channel"]

    bot_channel = bot.get_channel(bot_channel_id)
    if bot_channel is None:
        print(f"Error: The 'bot_channel' ID {bot_channel_id} does not correspond to any channel in the connected servers.")
        exit(1)

    print(f"Bot is ready! Using bot channel: {bot_channel.name} (ID: {bot_channel_id})")

async def handleExtension(action, name):
    bot_channel: discord.TextChannel = bot.get_channel(bot.global_config['bot_channel'])

    try:
        match action:
            case "load":
                await bot.load_extension(f'cogs.{name}')
                await bot_channel.send(f"extension **{name}** loaded successfully")
                return True
            case "unload":
                await bot.unload_extension(f'cogs.{name}')
                await bot_channel.send(f"extension **{name}** unloaded successfully")
                return True
            case "reload":
                await bot.reload_extension(f'cogs.{name}')
                await bot_channel.send(f"extension **{name}** reloaded successfully")
                return True
    except commands.ExtensionAlreadyLoaded:
        await bot_channel.send(f"**{name}** extension is already loaded")
    except commands.ExtensionNotFound:
        await bot_channel.send(f"extension **{name}** not found or not loaded")
    except Exception as e:
        if action == 'unload':
            await bot_channel.send(f"extension **{name}** not found or not loaded")    
        else:
            await bot_channel.send(f"Unexpected error with **{action} {name}** command : {e}")
    
    return False

@bot.command(name="reload")
@commands.has_permissions(administrator=True)
async def reload(ctx):
    bot_channel: discord.TextChannel = bot.get_channel(bot.global_config['bot_channel'])
    if ctx.channel.id == bot_channel.id:
        load_config()
        await bot_channel.send("config reloaded successfully")

@bot.command(name="extension")
@commands.has_permissions(administrator=True)
async def extension(ctx: commands.Context, action: str = None, name: str = None):
    bot_channel: discord.TextChannel = bot.get_channel(bot.global_config['bot_channel'])
    
    if ctx.channel.id == bot_channel.id:
        if action is None or name is None:
            await bot_channel.send("Error: Syntax error e.g **!load_extension load|unload|reload extension_name**")
            return
        await handleExtension(action, name)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    load_config()
    await load_extensions()
    await bot.start(os.getenv('TOKEN'))

asyncio.run(main())
