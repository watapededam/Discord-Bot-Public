import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

async def setup(client):
    await client.add_cog(Commands(client))
