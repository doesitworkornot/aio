from typing import List
from tgbot.models.test_user import TestUser

class Repo:
    """MySQL database abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    async def add_user(self, name, status, telegram_id, **kwargs) -> None:
        """Store user in DB"""

        sql = '''
            INSERT INTO tel_user (name, status, telegram_id)
            VALUES(%s, %s, %s)
            '''
        async with self.conn.cursor() as cur:
            await cur.execute(sql, [name, status, telegram_id])
            await self.conn.commit()

    async def del_user(self, db_user_id) -> None:
        """Delete user from DB"""

        sql = '''
            DELETE FROM tel_user WHERE id = %s
            '''
        async with self.conn.cursor() as cur:
            await cur.execute(sql, db_user_id)
            await self.conn.commit()

    async def list_users(self) -> List[TestUser]:
        '''Selects list of users'''

        sql = '''
            SELECT
                id, name, status, telegram_id
            FROM
                tel_user
            '''
        async with self.conn.cursor() as cur:
            await cur.execute(sql)
            return await cur.fetchall()
