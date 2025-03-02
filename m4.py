import json
import os
import re
from collections import defaultdict
from prettytable import PrettyTable
from colorama import Fore, Style, Back, init

# Инициализация colorama
init(autoreset=True)

# Параметры
KEY_W = 'usa'
PAGES_DIR = 'pars/pages/bt'
EV_JSON_PATH = 'ev.json'
IMPORTANT_CONTEXT_JSON = 'important_context.json'
ES_JSON_PATH = 'es.json'

# Размеры окон
WINDOW_SIZE = 150  # Для подсчёта категорий
CONTEXT_WORDS = 15  # Для отображения контекста

# Загрузка данных
with open(EV_JSON_PATH, 'r', encoding="utf-8") as f:
    es = json.load(f)

with open(IMPORTANT_CONTEXT_JSON, 'r', encoding="utf-8") as f:
    kw = json.load(f)

with open(ES_JSON_PATH, 'r', encoding="utf-8") as f:
    es_categories = json.load(f)

# Загрузка цветовой карты
color_map = {
    'v': Fore.BLUE,  # синий
    'g': Fore.GREEN,  # зелёный
    'r': Fore.RED,  # красный
    'b': Fore.YELLOW,  # жёлтый
}

# Создание словаря: слово -> категория и цвет
word_category_map = {}
word_color_map = {}
for category, words in es_categories.items():
    prefix = category[0].lower()
    color = color_map.get(prefix, '')
    for word in words:
        word_clean = word.strip().lower()
        if word_clean:
            word_category_map[word_clean] = category
            word_color_map[word_clean] = color


# Функция для выделения контекста
def highlight_context(words, index, total_words):
    start = max(index - CONTEXT_WORDS, 0)
    end = min(index + CONTEXT_WORDS + 1, total_words)  # Добавлено +1 для включения текущего слова
    context = words[start:end]
    highlighted = []
    for i, word in enumerate(context):
        word_lower = word.lower()
        if start + i == index:
            # Ключевое слово
            highlighted.append(f"{Back.YELLOW}{word}{Style.RESET_ALL}")
        elif word_lower in word_color_map:
            # Слово из категории
            color = word_color_map[word_lower]
            highlighted.append(f"{color}{word}{Style.RESET_ALL}")
        else:
            highlighted.append(word)
    return ' '.join(highlighted)


# Обработка файлов
files = os.listdir(PAGES_DIR)

for file in files:
    file_path = os.path.join(PAGES_DIR, file)
    with open(file_path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    text = data.get('text', '').lower()
    date = data.get('date', 'Дата не указана')

    # Поиск ключевых слов
    found = [m.start() for m in re.finditer(rf'\b{re.escape(KEY_W)}\b', text, re.IGNORECASE)]

    if found:
        print(f"\n\nДата: {date}\n")

        # Разбивка текста на слова
        words = re.findall(r'\b\w+\b', text)
        total_words = len(words)

        # Создание обратного словаря для категорий
        keyword_counts = defaultdict(lambda: defaultdict(int))

        # Приведение ключевых слов к нижнему регистру
        kw_lower = [word.lower() for word in kw]

        for pos in found:
            # Определение индекса слова
            word_index = len(re.findall(r'\b\w+\b', text[:pos]))  # Убрано -1
            if 0 <= word_index < total_words:
                # Определение окна для подсчёта
                start = max(word_index - WINDOW_SIZE, 0)
                end = min(word_index + WINDOW_SIZE + 1, total_words)
                context = words[start:end]

                for i, context_word in enumerate(context):
                    if (start + i) == word_index:
                        continue  # Пропуск ключевого слова
                    category = word_category_map.get(context_word)
                    if category:
                        keyword_counts[KEY_W][category] += 1

        # Вывод таблицы
        table = PrettyTable()
        table.field_names = ["Группа", "Количество"]
        table.align["Группа"] = "l"

        counts = keyword_counts.get(KEY_W, {})
        if counts:
            for category, count in counts.items():
                table.add_row([category, count])
        else:
            table.add_row(["Нет связанных слов в контексте.", ""])

        print(table)
        print()

        # Вывод контекста для каждого вхождения
        for pos in found:
            word_index = len(re.findall(r'\b\w+\b', text[:pos]))  # Убрано -1
            if 0 <= word_index < total_words:
                context_str = highlight_context(words, word_index, total_words)
                print(context_str)
                # print("\n" + "-" * 80 + "\n")
