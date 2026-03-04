import models.database as db
import models.scraper as scr
import models.news as news
import asyncio


async def main() -> None:
    sources = ["https://dzen.ru/news"]
    dsn = "postgresql://postgres:123@localhost:5432/news_parser"
    database = db.Database(dsn)
    scraper = scr.Scraper(sources)
    try:
        await database.connect()
        news_list = await scraper.scrape()
        await database.save(news_list)
        print(f"Сохранено {len(news_list)} новостей")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await database.close()


if __name__ == "__main__":
    asyncio.run(main())
