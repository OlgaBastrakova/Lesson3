 

# Открытие файла и чтение содержимого в переменную
with open('referat.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Подсчет длины строки
text_length = len(text)
print("Длина строки:", text_length)

# Подсчет количества слов
word_count = len(text.split())
print("Количество слов:", word_count)

# Замена точек на восклицательные знаки
new_text = text.replace('.', '!')
print("Текст с заменой точек на восклицательные знаки:")
print(new_text)

# Сохранение результата в файл
with open('referat2.txt', 'w', encoding='utf-8') as file:
    file.write(new_text)