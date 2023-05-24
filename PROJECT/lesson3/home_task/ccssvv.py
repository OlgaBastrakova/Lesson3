import csv


# Создание списка словарей
people = [
    {'name': 'Маша', 'age': 25, 'job': 'Scientist'},
    {'name': 'Вася', 'age': 8, 'job': 'Programmer'},
    {'name': 'Эдуард', 'age': 48, 'job': 'Big boss'},
]

# Запись содержимого списка словарей в файл CSV
with open('people.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['name', 'age', 'job'])
    writer.writeheader()
    for person in people:
        writer.writerow(person)