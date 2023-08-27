import asyncpg
from langchain.utilities import SQLDatabase

from setting import setting


class Pool:
    async def open_pool(self):
        self.pool = await asyncpg.create_pool(dsn=setting.DBSTRING)

    async def close_pool(self):
        await self.pool.close()

    async def terminate_pool(self):
        await self.pool.terminate()

    def get_pool(self):
        return self.pool

    def get_db_langchain(self):
        return SQLDatabase.from_uri(setting.DBSTRING)


db = Pool()
