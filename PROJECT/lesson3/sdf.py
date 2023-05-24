# Задание 2
# Дан список учеников, нужно вывести самое часто повторящееся имя
# Пример вывода:
# Самое частое имя среди учеников: Маша
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Оля'},
]
name_counts = {}
most_common_name = None
max_count = 0

for student in students:
    name = student['first_name']
    if name in name_counts:
        name_counts[name] += 1
    else:
        name_counts[name] = 1

most_common_name = max(name_counts, key=name_counts.get)

print(f"Самое частое имя среди учеников: {most_common_name}")