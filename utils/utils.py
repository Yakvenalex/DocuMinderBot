import re


def transform_string(input_string):
    # Разделяем строку по запятым
    words = input_string.split(',')
    # Убираем лишние пробелы, приводим к нижнему регистру и заменяем множественные пробелы на один
    cleaned_words = [re.sub(' +', ' ', word.strip().lower()) for word in words if word.strip()]
    # Объединяем слова обратно в строку через запятую
    result = ','.join(cleaned_words)
    return result