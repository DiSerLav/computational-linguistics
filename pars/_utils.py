import re

import unicodedata
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords


# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def parse_relative_url(url: str, base_url: str) -> str:
    """
    Позволяет привести все ссылки к абсолютным

    :param url: Текущая ссылка.
    :param base_url: Ссылка, содержащая базовый url
    :return: Абсолютная ссылка
    """
    if url.startswith('http'):
        return url

    if url.startswith('/'):
        return f'https://{base_url.replace('https://', '').split('/')[0]}{url}'

    return f'{base_url}/{url}'


my_stopwords = [
    'pdf', 'kb', 'dr'
]


def semantic_cleaning(text):
    # Токенизация текста
    words = word_tokenize(text)

    # Удаление стоп-слов
    stop_words = set(stopwords.words('english') + stopwords.words('german') + my_stopwords)
    words = [word for word in words if word.lower() not in stop_words]

    # Лемматизация слов
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # Соединение слов обратно в текст
    cleaned_text = ' '.join(words)
    return cleaned_text


def clean_text(text, strict=False):
    # Удаление всех неразрывных пробелов
    text = text.replace('\xa0', ' ')
    # Нормализация текста для удаления специальных символов
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Замена всех странных спецсимволов
    if strict:
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower()
        text = semantic_cleaning(text)
        text = re.sub(r'\d+', ' ', text).strip()

    # Удаление лишних пробелов
    return re.sub(r'\s+', ' ', text).strip()
