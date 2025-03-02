import json
import re
from colorama import Fore, Style, init, Back

# Инициализация colorama
init(autoreset=True)

# Загрузка ключевых слов
with open('important_context.json', 'r', encoding="utf-8") as f:
    kw = json.load(f)  # массив с ключевыми словами

with open('es.json', 'r', encoding="utf-8") as f:
    es = json.load(f)

with open('pars/pages/bt.txt', 'r', encoding="utf-8") as f:
    text = f.read()

# Словарь с эмоциями и соответствующими словами

# Определяем цвет для каждой категории по первой букве ключа
color_map = {
    'v': Fore.BLUE,       # синий
    'g': Fore.GREEN,      # зелёный
    'r': Fore.RED,        # красный
    'b': Fore.YELLOW,     # жёлтый
}


# Создаем обратный словарь: слово -> цвет
word_color_map = {}
for category, words in es.items():
    prefix = category[0].lower()  # первая буква для цвета
    color = color_map.get(prefix, '')
    for word in words:
        word_clean = word.strip().lower()
        if word_clean:
            word_color_map[word_clean] = color

# Разбиваем текст на слова с сохранением порядка
words = re.findall(r'\b\w+\b', text)

# Приводим ключевые слова к нижнему регистру для сравнения
kw_lower = [word.lower() for word in kw]

# Ищем индексы ключевых слов и выводим контекст с выделением
for i, word in enumerate(words):
    word_lower = word.lower()
    if word_lower in kw_lower:
        # Определяем границы контекста
        start = max(i - 12, 0)
        end = min(i + 13, len(words))
        # Получаем контекст
        context = words[start:end]
        # Обрабатываем каждое слово в контексте
        highlighted_context = []
        for j, context_word in enumerate(context):
            context_word_lower = context_word.lower()
            if j == i - start:
                # Это ключевое слово - выделяем жирным
                highlighted = f"{Back.YELLOW}{context_word}{Style.RESET_ALL}"
            elif context_word_lower in word_color_map:
                # Это слово из окружения - выделяем цветом
                color = word_color_map[context_word_lower]
                highlighted = f"{color}{context_word}{Style.RESET_ALL}"
            else:
                # Обычное слово
                highlighted = context_word
            highlighted_context.append(highlighted)
        # Выводим контекст
        print(' '.join(highlighted_context))