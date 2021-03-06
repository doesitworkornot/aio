from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.services.repository import Repo


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def pre_process(self, obj, data, *args):
        data['db'] = await self.pool.acquire()
        data['repo'] = Repo(data['db'])

    async def post_process(self, obj, data, *args):
        data.pop('repo', None)
        if 'db' in data:
            await self.pool.release(data.pop('db'))
