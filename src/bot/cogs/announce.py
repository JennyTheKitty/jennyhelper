from typing import List
import asyncio
import re

import discord
from discord.ext import commands

CDN_LINK_PATTERN = r"(https:\/\/(?:cdn|media)\.discordapp\.(?:com|net)\/\S*)"

PING_ROLE_NAME = "JFF New Content Ping"
URL = "https://justfor.fans/JennyKittyBaby"
CHANNEL = "jenny-new-content"
AUTHOR_USERNAME = "JennyKittyBaby"
AUTHOR_AVATAR_URL = "https://cdn.discordapp.com/attachments/263324164117495809/808068333140049920/5w6Oqh4e_400x400.png"

KEYCAP_DIGITS = {0: "0️⃣", 1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣"}


def author_reaction(emojis: List[str], author: discord.Member, msg: discord.Message):
    def check(reaction: discord.Reaction, user: discord.Member):
        x = (
            user.id == author.id
            and reaction.message.id == msg.id
            and str(reaction.emoji) in emojis
        )
        return x

    return check


class Announce(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @property
    def webhook_name(self):
        return f"{self.bot.user.name} Proxy"

    async def get_webhook(self, channel: discord.TextChannel):
        for webhook in await channel.webhooks():
            if webhook.name == self.webhook_name:
                break
        else:
            webhook = await channel.create_webhook(name=self.webhook_name)

        return webhook

    async def receive_images(self, ctx: commands.Context, max_images: int):
        ask_msg = await ctx.channel.send(
            "Alright, please send images to go along with it. Click the 🆗 below when done."
        )
        await ask_msg.add_reaction("🆗")

        def get_pic(msg: discord.Message):
            if len(msg.attachments) > 0:
                return msg.attachments[0].url
            else:
                search = re.search(CDN_LINK_PATTERN, msg.content)
                if search:
                    return search.group(1)

        def image_check(msg: discord.Message):
            return ctx.author == msg.author and get_pic(msg) is not None

        reaction_task = asyncio.create_task(
            self.bot.wait_for(
                "reaction_add",
                check=author_reaction(["🆗"], ctx.author, ask_msg),
            )
        )

        images = []
        while True:
            image_task = asyncio.create_task(
                self.bot.wait_for("message", check=image_check)
            )
            done, pending = await asyncio.wait(
                [reaction_task, image_task], return_when=asyncio.FIRST_COMPLETED
            )
            if reaction_task in done:
                image_task.cancel()
                break

            if image_task in done:
                images.append(get_pic(image_task.result()))
                await ask_msg.add_reaction(KEYCAP_DIGITS[len(images)])
                if len(images) >= max_images:
                    reaction_task.cancel()
                    break

        return images

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid sub command passed...")

    @announce.command()
    async def jff(self, ctx: commands.Context, type: str, direct_link: str):
        if type not in ['video', 'images', 'image', 'imgs']:
            await ctx.send('Type not recognized.')
            return

        await ctx.send("Please send description.")

        description_msg = await self.bot.wait_for(
            "message", check=lambda msg: msg.author == ctx.author
        )
        description = description_msg.content

        images = await self.receive_images(ctx, 1 if type == 'video' else 4)

        if len(images) == 0:
            await ctx.send("No images found. Cancelling.")
            return

        ping_role = discord.utils.get(ctx.guild.roles, name=PING_ROLE_NAME)

        embeds = [
            discord.Embed(
                title="New JFF post!", url=direct_link, description=description
            )
            .set_image(url=images[0])
            .set_author(
                name="JustFor.Fans/JennyKittyBaby",
                url="https://justfor.fans/JennyKittyBaby",
                icon_url="https://cdn.discordapp.com/attachments/263324164117495809/808060124995387392/7be144a.png",
            )
        ]
        for image in images[1:]:
            embeds.append(discord.Embed(url=direct_link).set_image(url=image))

        kwargs = dict(
            embeds=embeds,
            username=AUTHOR_USERNAME,
            avatar_url=AUTHOR_AVATAR_URL,
        )

        preview_msg = await (await self.get_webhook(ctx.channel)).send(
            "__**This is a preview!**__\n(react 👍 to send, 👎 to cancel)",
            wait=True,
            **kwargs,
        )
        await preview_msg.add_reaction("👍")
        await preview_msg.add_reaction("👎")

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add",
                timeout=60.0,
                check=author_reaction(["👍", "👎"], ctx.author, preview_msg),
            )
        except asyncio.TimeoutError:
            await ctx.channel.send("Timed out.")
            return

        if str(reaction) == "👎":
            await ctx.channel.send("Cancelling.")
            return

        channel = discord.utils.get(ctx.guild.text_channels, name=CHANNEL)

        await (await self.get_webhook(channel)).send(
            f"{ping_role.mention}", **kwargs
        )
