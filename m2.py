import json
import re
from collections import defaultdict
from prettytable import PrettyTable

# Загрузка ключевых слов
with open('important_context.json', 'r', encoding="utf-8") as f:
    kw = json.load(f)  # массив с ключевыми словами

with open('ev.json', 'r', encoding="utf-8") as f:
    es = json.load(f)

with open('pars/pages/bt.txt', 'r', encoding="utf-8") as f:
    text = f.read().lower()

# Создаем обратный словарь: слово -> категория
word_category_map = {}
for category, words in es.items():
    for word in words:
        word_clean = word.strip().lower()
        if word_clean:
            word_category_map[word_clean] = category

# Разбиваем текст на слова с сохранением порядка
words = re.findall(r'\b\w+\b', text)

# Приводим ключевые слова к нижнему регистру для сравнения
kw_lower = [word.lower() for word in kw]

# Инициализируем словарь для подсчёта
keyword_counts = defaultdict(lambda: defaultdict(int))

# Определяем размер окна контекста
window_size = 150

# Проходим по всем словам и ищем ключевые
for i, word in enumerate(words):
    word_lower = word.lower()
    if word_lower in kw_lower:
        # Определяем границы контекста
        start = max(i - window_size, 0)
        end = min(i + window_size + 1, len(words))
        # Получаем контекст
        context = words[start:end]
        # Подсчитываем категории в контексте, исключая само ключевое слово
        for j, context_word in enumerate(context):
            if j == i - start:
                continue  # Пропускаем ключевое слово
            context_word_lower = context_word.lower()
            category = word_category_map.get(context_word_lower)
            if category:
                keyword_counts[word_lower][category] += 1

# Вывод результатов с использованием PrettyTable
for keyword, counts in keyword_counts.items():
    print(f"Ключевое слово: {keyword}")
    table = PrettyTable()
    table.field_names = ["Группа", "Количество"]
    table.align["Группа"] = "l"
    if counts:
        for category, count in counts.items():
            table.add_row([category, count])
    else:
        table.add_row(["Нет связанных слов в контексте.", ""])
    print(table)
    print()
