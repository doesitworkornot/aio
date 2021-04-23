import asyncio
import aiomysql
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
)


async def create_pool(user, password, database, host, loop):
    db = await aiomysql.create_pool(
        user=user, password=password, db=database,
        host=host, port=3306, use_unicode=True, charset='utf8', loop=loop)
    return db
    #raise NotImplementedError  # TODO check your db connector


async def main():
    logger.error('Starting bot')
    config = load_config('bot.ini')

    if config.tg_bot.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()

    loop = asyncio.get_event_loop()
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        loop=loop,
    )

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_user(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
