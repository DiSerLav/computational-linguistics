"""
Абстрактные классы.
"""
import abc

import requests
from bs4 import BeautifulSoup

from pars.schemas import PageSchema, LinkSchema


class Page(abc.ABC):
    """
    Абстрактный класс для страниц
    """

    _url: str
    _response: requests.Response
    _soup: BeautifulSoup

    _data: PageSchema

    @abc.abstractmethod
    def parse(self) -> None:
        """
        Парсинг страницы
        """

    @abc.abstractmethod
    def get_data(self) -> PageSchema:
        """
        Получение информации о странице
        :return:
        """

    @property
    @abc.abstractmethod
    def url(self) -> str:
        """
        Возвращает url страницы

        :return: Ссылка на текущую страницу
        """

    @property
    @abc.abstractmethod
    def plain_text(self) -> str:
        """
        Возвращает текст страницы без разметки и ссылок

        :return: Текст страницы
        """

    @property
    @abc.abstractmethod
    def links(self) -> list[LinkSchema]:
        """
        Возвращает заголовок страницы

        :return: Заголовок страницы
        """

    @property
    @abc.abstractmethod
    def images(self) -> list[LinkSchema]:
        """
        Возвращает ссылки на изображения

        :return: Ссылки на изображения
        """

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта

        :return: Строковое представление объекта
        """
