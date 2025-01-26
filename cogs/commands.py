import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_error_message(self, error, context="General"):
        cog_name = self.__class__.__name__
        bot_channel = self.bot.get_channel(self.bot.global_config['bot_channel'])
        if bot_channel:
            await bot_channel.send(f"Error in {cog_name} - {context}: {error}")
        else:
            print(f"Error in {cog_name} - {context}: {error}")

    @commands.command(name="Hello")
    async def hello(self, ctx):
        bot_channel = self.bot.get_channel(self.bot.global_config['bot_channel'])
        if ctx.channel.id == bot_channel.id:
            await bot_channel.send("Hello")

    @commands.command(name="AdminCommand")
    @commands.has_permissions(administrator=True)
    async def admin_command(self, ctx):
        bot_channel = self.bot.get_channel(self.bot.global_config['bot_channel'])
        if ctx.channel.id == bot_channel.id:
            await bot_channel.send("This is an admin-only command!")

    @commands.command(name="error_example")
    async def error_example(self, ctx):
        try:
            # Example of raising an error to trigger the send_error_message function
            raise ValueError("This is a test error.")
        except Exception as e:
            await self.send_error_message(str(e), context="error_example")

async def setup(client):
    await client.add_cog(Commands(client))
