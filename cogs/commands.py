import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Hello")
    async def hello(self, ctx):
        try:
            await ctx.send("Hello")
        except Exception as e:
            await self.bot.send_error_message(str(e), context=ctx)

    @commands.command(name="AdminCommand")
    @commands.has_permissions(administrator=True)
    async def admin_command(self, ctx):
        try:
            bot_channel = self.bot.get_channel(self.bot.global_config['bot_channel'])
            if ctx.channel.id == bot_channel.id:
                await bot_channel.send("This is an admin-only command!")
        except Exception as e:
            await self.bot.send_error_message(str(e), context=ctx)

    @commands.command(name="test_error")
    @commands.has_permissions(administrator=True)
    async def test_error(self, ctx):
        try:
            command_name = ctx.command.name
            user = ctx.author
            channel = ctx.channel.name
            raise ValueError(f"Simulated error triggered by {user} while executing '{command_name}' in #{channel}.")
        except Exception as e:
            await self.bot.send_error_message(str(e), context=ctx)

async def setup(client):
    await client.add_cog(Commands(client))
