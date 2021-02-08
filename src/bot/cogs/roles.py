from typing import Optional, Mapping

import discord
from discord.ext import commands

from bot.db.models import RoleMessage


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def roles(self, ctx: commands.Context, msg: Optional[discord.Message] = None):
        if msg is None:
            if ctx.message.reference:
                if ctx.message.reference.resolved and isinstance(
                    ctx.message.reference.resolved, discord.Message
                ):
                    try:
                        msg = await ctx.fetch_message(ctx.message.reference.message_id)
                    except discord.NotFound:
                        await ctx.reply("Message could not be found.")
            else:
                await ctx.reply("Message could not be found.")

        await ctx.message.delete()

        requested: Mapping[str, discord.Role] = self.get_roles(ctx.guild, msg.content)

        await RoleMessage.get_or_create(id=msg.id)

        for emoji in requested.keys():
            await msg.add_reaction(emoji)

        for emoji in set(str(r) for r in msg.reactions) - set(requested.keys()):
            await msg.clear_reaction(emoji)

    def get_roles(self, guild: discord.Guild, text: str) -> Mapping[str, discord.Role]:
        roles = {}

        for line in text.split("\n"):
            candidate = [x.strip() for x in line.lower().split("-", maxsplit=2)]
            if len(candidate) < 2:
                continue

            for role in guild.roles:
                if (
                    role.name.lower() == candidate[1]
                    or role.name.lower().strip(candidate[0]).strip().lower() == candidate[1]
                ):
                    roles[candidate[0]] = role
        return roles

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if not await RoleMessage.exists(id=payload.message_id):
            return

        msg = await (self.bot.get_channel(payload.channel_id)).fetch_message(
            payload.message_id
        )

        roles = self.get_roles(self.bot.get_guild(payload.guild_id), msg.content)

        await payload.member.add_roles(roles[str(payload.emoji)])

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if not await RoleMessage.exists(id=payload.message_id):
            return

        msg = await (self.bot.get_channel(payload.channel_id)).fetch_message(
            payload.message_id
        )

        guild = self.bot.get_guild(payload.guild_id)

        roles = self.get_roles(guild, msg.content)

        member = await guild.fetch_member(payload.user_id)

        await member.remove_roles(roles[str(payload.emoji)])
