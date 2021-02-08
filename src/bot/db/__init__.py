import logging

from tortoise import Tortoise

logger = logging.getLogger("db")


TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["bot.db.models"],
            "default_connection": "default",
        },
    },
}


async def init():
    logger.debug('Init start')
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    logger.info("Connected")


async def close():
    logger.info("Closing connection")
    await Tortoise.close_connections()
