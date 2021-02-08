from typing import Optional, Mapping

import discord
from discord.ext import commands

from bot.db.models import RoleMessage


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def dump(self, ctx: commands.Context):
        print(ctx.message)