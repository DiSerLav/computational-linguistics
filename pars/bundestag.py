from datetime import datetime
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from pars._classes import Page
from pars._utils import parse_relative_url, clean_text
from pars.schemas import PageSchema, LinkSchema


class BtPage(Page):
    """
    Класс для парсинга страницы Bundestag
    """

    def __init__(self, url, date: datetime=None):
        self._url = url
        self._response = requests.get(url, timeout=5)
        self._date = date
        if self._response.status_code != 200:
            raise ValueError(f'Unable to fetch page {self.url}: {self._response.status_code}')

        self._soup = BeautifulSoup(self._response.text, 'html.parser')

        self._soup = self._soup.find('article') or self._soup

        self.parse()

    def parse(self) -> None:
        pass

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def url(self):
        return self._url

    @property
    def links(self):
        return [LinkSchema(
            url=parse_relative_url(link.get('href'), self.url),
            title=link.get_text(strip=True) or None
        ) for link in self._soup.find_all('a')]

    @property
    def images(self) -> list[LinkSchema]:
        return [LinkSchema(
            url=parse_relative_url(image['src'], self.url),
            title=image.get('alt')
        ) for image in self._soup.find_all('img')]

    @property
    def plain_text(self) -> str:
        text = self._soup.get_text(strip=True, separator=' ')
        return clean_text(text, strict=True)

    @property
    def title(self) -> str:
        try:
            return self._soup.find('h1').get_text(strip=True)
        except AttributeError:
            return "None"

    @property
    def __hash__(self):
        return hash(self.url)

    def get_data(self) -> PageSchema:
        ps = PageSchema(url=self.url, text=self.plain_text,
                        links=self.links, images=self.images,
                        title=self.title, date=self._date)
        return ps

    def __str__(self):
        return f'<Url: {self.url}>'


def main():
    url = 'https://www.bundestag.de/dokumente/textarchiv/2021/kw34-de-afghanistan-855300'

    page = BtPage(url)
    pprint(page.get_data().model_dump())


if __name__ == '__main__':
    main()
