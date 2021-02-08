import os

import asyncio
import uvloop
from dotenv import load_dotenv, find_dotenv

import bot


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    load_dotenv(find_dotenv())
    bot.run(token=os.getenv("DISCORD_BOT_TOKEN"))
