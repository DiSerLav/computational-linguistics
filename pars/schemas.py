from datetime import datetime
from typing import Optional

import pydantic


class PageSchema(pydantic.BaseModel):
    """
    Схема страницы

    :var title: Заголовок страницы
    :var url: Ссылка на страницу

    :var text: Текст страницы
    :var date: Дата публикации
    :var author: Автор

    :var links: Ссылки на другие страницы или материалы
    """

    title: Optional[str] = None
    url: str

    text: Optional[str]
    date: Optional[str] = None
    author: Optional[str] = None

    links: list["LinkSchema"] = []
    images: list["LinkSchema"] = []


class LinkSchema(pydantic.BaseModel):
    """
    Схема ссылки

    :var title: Заголовок ссылки
    :var url: Ссылка
    """

    title: Optional[str]
    url: str
