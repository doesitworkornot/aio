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
