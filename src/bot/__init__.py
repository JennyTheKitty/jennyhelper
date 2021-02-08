import logging
import asyncio

import discord
from discord.ext import commands

from bot import cogs, db

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
)


class JennyHelperBot(commands.Bot):
    class Help(discord.ext.commands.DefaultHelpCommand):
        def __init__(self):
            super().__init__()
            self.no_category = 'Other'

    def __init__(self):
        super().__init__(command_prefix='!', help_command=self.Help())

        self.logger = logging.getLogger("JennyHelperBot")

        self.loop.create_task(self.db_task())

        for cog in map(cogs.__dict__.get, cogs.__all__):
            self.add_cog(cog(self))

    async def on_ready(self):
        self.logger.info('Logged in as %s (%s) ', self.user.name, self.user.id)
        await self.change_presence(activity=discord.Game("!help"))

    async def db_task(self):
        try:
            await db.init()
            while not self.is_closed():
                await asyncio.sleep(60)
        finally:
            await db.close()

    async def on_error(self, event_name, *args, **kwargs):
        self.logger.exception(
            f"Exception while handling event {event_name}"
        )


def run(*, token: str):
    bot = JennyHelperBot()
    bot.run(token)
