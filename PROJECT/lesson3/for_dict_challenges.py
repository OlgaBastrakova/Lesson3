# Задание 1
# Дан список учеников, нужно посчитать количество повторений каждого имени ученика
# Пример вывода:
# Вася: 1
# Маша: 2
# Петя: 2

students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Петя'},
]
print("Задание 1")
name_counts = {}

for student in students:
    name = student['first_name']
    if name in name_counts:
        name_counts[name] += 1
        
    else:
        name_counts[name] = 1

for name, count in name_counts.items():
    print(f"{name}: {count}")


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
print("Задание 2")
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

# Задание 3
# Есть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе.
# Пример вывода:
# Самое частое имя в классе 1: Вася
# Самое частое имя в классе 2: Маша

school_students = [
    [  # это – первый класс
        {'first_name': 'Вася'},
        {'first_name': 'Вася'},
    ],
    [  # это – второй класс
        {'first_name': 'Маша'},
        {'first_name': 'Маша'},
        {'first_name': 'Оля'},
    ],[  # это – третий класс
        {'first_name': 'Женя'},
        {'first_name': 'Петя'},
        {'first_name': 'Женя'},
        {'first_name': 'Саша'},
    ],
]
print("Задание 3")
from collections import Counter
for i, class_students in enumerate(school_students):
    names = [student['first_name'] for student in class_students]
    count = Counter(names)
    most_common_name = count.most_common(1)[0][0]
    print(f"Самое частое имя в классе {i+1}: {most_common_name}")


# Задание 4
# Для каждого класса нужно вывести количество девочек и мальчиков в нём.
# Пример вывода:
# Класс 2a: девочки 2, мальчики 0 
# Класс 2б: девочки 0, мальчики 2

school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '2б', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
    {'class': '2б', 'students': [{'first_name': 'Даша'}, {'first_name': 'Олег'}, {'first_name': 'Маша'}]},
]
is_male = {
    'Олег': True,
    'Маша': False,
    'Оля': False,
    'Миша': True,
    'Даша': False,
}
print("Задание 4")
for class_info in school:
    class_name = class_info['class']
    students = class_info['students']
    num_girls = 0
    num_boys = 0
    for student in students:
        name = student['first_name']
        if is_male[name]:
            num_boys += 1
        else:
            num_girls += 1
    print(f"Класс {class_name}: девочки {num_girls}, мальчики {num_boys}")


# Задание 5
# По информации о учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков
# Пример вывода:
# Больше всего мальчиков в классе 3c
# Больше всего девочек в классе 2a

school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
    'Маша': False,
    'Оля': False,
    'Олег': True,
    'Миша': True,
}
print("Задание 5")
for class_info in school:
    class_name = class_info['class']
    students = class_info['students']
    num_girls = 0
    num_boys = 0
    for student in students:
        name = student['first_name']
        if is_male[name]:
            num_boys += 1
        else:
            num_girls += 1
    if num_boys > num_girls:
        print(f"Больше всего  в классе {class_name}:  мальчиков {num_boys}")
    else:
        print(f"Больше всего  в классе {class_name}:  девочек {num_girls}")
  

