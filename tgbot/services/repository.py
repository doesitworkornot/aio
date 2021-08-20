from typing import List

class Repo:
    """MySQL database abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    async def add_user(self, new_id, new_name, new_role, **kwargs) -> None:
        """Store user in DB"""

        sql = '''
            INSERT INTO tel_user (name, status, telegram_id)
            VALUES(%s, %s, %s)
            '''
        async with self.conn.cursor() as cur:
            print(new_role, new_name, new_id)
            await cur.execute(sql, [new_name, new_role, new_id])
            await self.conn.commit()

    async def del_user(self, db_user_id) -> None:
        """Delete user from DB"""

        sql = '''
            DELETE FROM tel_user WHERE id = %s
            '''
        async with self.conn.cursor() as cur:
            await cur.execute(sql, db_user_id)
            await self.conn.commit()

    async def list_users(self):
        '''Selects list of users'''

        sql = '''
            SELECT id, name, status, telegram_id FROM tel_user
            '''
        async with self.conn.cursor() as cur:
            await cur.execute(sql)
            return await cur.fetchall()

    async def status_check(self, user_id):
        sql = f'''
            SELECT status FROM tel_user WHERE telegram_id = {user_id}
            '''
        async with self.conn.cursor() as cur:
            await cur.execute(sql)
            return await cur.fetchall()
