import asyncio
import aiohttp
from datetime import datetime
from news import News
from bs4 import BeautifulSoup

# url для теста: https://dzen.ru/news


class Scraper:
    __source: list[str]
    __timeout: aiohttp.ClientTimeout
    __headers: dict
    __session: aiohttp.ClientSession

    def __init__(self, source: list[str]):
        self.__source = source
        self.__headers = {'User-Agent': 'Mozilla/5.0'}
        self.__timeout = aiohttp.ClientTimeout(total=10)

    async def _fetch_get(self, url: str) -> str:
        response = await self.__session.get(url, timeout=self.__timeout)
        return await response.text()

    async def _parse(self, html: str, url: str) -> list[News]:
        page = html
        filteredNews = []
        allNews = []
        soup = BeautifulSoup(page, "html.parser")
        allNews = soup.find_all(
            'a', class_="news-site--card-top-avatar__rootElement-1U")

        for data in allNews:
            title_elem = data.find(
                'p', class_="news-site--card-top-avatar__text-SL")
            if title_elem:
                news_url = data.get("href")
                title = title_elem.text.strip()
                news = News(news_url, title)
                filteredNews.append(news)

        return filteredNews

    async def scrape(self) -> list[News]:
        async with aiohttp.ClientSession(headers=self.__headers, timeout=self.__timeout) as session:
            self.__session = session
            tasks = []
            all_news = []
            for url in self.__source:
                tasks.append(self._fetch_get(url))
            htmls = await asyncio.gather(*tasks, return_exceptions=True)
            for html, url in zip(htmls, self.__source):
                if isinstance(html, Exception):
                    print(f"Ошибка при загрузке {url}: {html}")
                    continue
                try:
                    news_list = await self._parse(html, url)
                    all_news.extend(news_list)
                except Exception as e:
                    print(f"Ошибка при парсинге {url}: {e}")

        return all_news
