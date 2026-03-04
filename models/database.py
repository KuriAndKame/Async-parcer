import asyncpg
from .news import News


class Database:
    __dsn: str
    __pool: asyncpg.Pool

    def __init__(self, dsn):
        self.__dsn = dsn

    async def connect(self):
        self.__pool = await asyncpg.create_pool(self.__dsn)

    async def save(self, news_list: list[News]):
        for news in news_list:
            await self.__pool.execute('''INSERT INTO news(url, title) VALUES ($1, $2) ON CONFLICT(url) DO NOTHING''', news.url, news.title)

    async def get_all(self, limit=100) -> list[News]:
        rows = await self.__pool.fetch('''SELECT * FROM news LIMIT $1 ''', limit)
        return [News(row['url'], row['title']) for row in rows]

    async def close(self):
        await self.__pool.close()
