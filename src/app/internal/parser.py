import asyncio
from typing import List, Dict, Any

import aiohttp
from LxmlSoup import LxmlSoup

from app.internal.services.article_service import add_article
from app.internal.services.hub_service import get_hubs, get_hub_by_parameter
from config.settings import WAIT_FOR_HUBS_UPDATE


class AsyncHabrParser:
    def __init__(self):
        self.BASE = 'https://habr.com'
        self.hubs = get_hubs()

    async def start_parser(self):
        async with asyncio.TaskGroup() as tg:
            print(f'Parser is starting. Parsing {len(self.hubs)} hubs')
            [tg.create_task(self.parse_hub(hub.url, hub.parse_period)) for hub in self.hubs]
            tg.create_task(self.check_for_new_hubs(tg))

    async def check_for_new_hubs(self, tg: asyncio.TaskGroup):
        while True:
            await asyncio.sleep(WAIT_FOR_HUBS_UPDATE)
            hubs = get_hubs()
            new_hubs = list(set(hubs) - set(self.hubs))
            self.hubs = hubs
            print(f'Add {len(new_hubs)} hubs with urls {[new_hub.url for new_hub in new_hubs]}')
            [tg.create_task(self.parse_hub(hub.url, hub.parse_period)) for hub in new_hubs]

    async def parse_hub(self, hub_url: str, period: int):
        while True:
            hub = get_hub_by_parameter('url', hub_url)
            if not hub:
                print(f'Delete 1 hub with url {hub_url}')
                return
            articles_url = await self.parse_hub_articles_url(hub_url)
            tasks = [self.parse_article(self.BASE + article_url) for article_url in articles_url]
            articles = await asyncio.gather(*tasks)
            for article in articles:
                if article:
                    add_article(article_title=article['title'],
                                article_url=article['article_url'],
                                created_at=article['datetime'],
                                author_url=self.BASE + article['author_url'],
                                author_name=article['author_name'],
                                body=article['body'],
                                hub=hub)
            await asyncio.sleep(period)

    @staticmethod
    async def parse_hub_articles_url(hub_url: str) -> List[str]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(hub_url) as resp:
                    html_content = await resp.text()
        except aiohttp.client_exceptions.ClientConnectorError:
            print(f'Error connecting {hub_url}')
            return []

        soup = LxmlSoup(html_content)
        articles = soup.find_all('article', class_='tm-articles-list__item')
        articles_url = [article.find_all('a', class_='tm-title__link')[0].get('href') for article in
                        articles]
        return articles_url

    @staticmethod
    async def parse_article(article_url: str) -> Dict[str, Any] | None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(article_url) as resp:
                    html_content = await resp.text()
                    if resp.status == 503:  # habr blocked request
                        return
        except aiohttp.client_exceptions.ClientConnectorError:
            print(f'Error connecting {article_url}')
            return

        print(f'Parsing {article_url}')
        soup = LxmlSoup(html_content)

        title = soup.find_all('h1', class_='tm-title tm-title_h1')[0].find_all('span')[0].text()

        datetime_block = soup.find_all('span', class_='tm-article-datetime-published')[0].find_all('time')[0]
        datetime = datetime_block.get('datetime')

        author_block = soup.find_all('a', class_='tm-user-info__username')[0]
        author_url = author_block.get('href')
        author_name = author_block.text()

        article_body = soup.find_all('div', class_='tm-article-body')[0].text()

        return {'title': title,
                'datetime': datetime,
                'author_url': author_url,
                'author_name': author_name,
                'body': article_body,
                'article_url': article_url}
