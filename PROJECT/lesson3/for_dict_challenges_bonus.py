"""
Пожалуйста, приступайте к этой задаче после того, как вы сделали и получили ревью ко всем остальным задачам
в этом репозитории. Она значительно сложнее.


Есть набор сообщений из чата в следующем формате:

```
messages = [
    {
        "id": "efadb781-9b04-4aad-9afe-e79faef8cffb",
        "sent_at": datetime.datetime(2022, 10, 11, 23, 11, 11, 721),
        "sent_by": 46,  # id пользователя-отправителя
        "reply_for": "7b22ae19-6c58-443e-b138-e22784878581",  # id сообщение, на которое это сообщение является ответом (может быть None)
        "seen_by": [26, 91, 71], # идентификаторы пользователей, которые видели это сообщение
        "text": "А когда ревью будет?",
    }
]
```

Так же есть функция `generate_chat_history`, которая вернёт список из большого количества таких сообщений.
Установите библиотеку lorem, чтобы она работала.

Нужно:
1. Вывести айди пользователя, который написал больше всех сообщений.
2. Вывести айди пользователя, на сообщения которого больше всего отвечали.
3. Вывести айди пользователей, сообщения которых видело больше всего уникальных пользователей.
4. Определить, когда в чате больше всего сообщений: утром (до 12 часов), днём (12-18 часов) или вечером (после 18 часов).
5. Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).

Весь код стоит разбить на логические части с помощью функций.
"""
import random
import uuid
import datetime
from typing import List, Dict, Any
import lorem
from collections import Counter

# 5. Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).
messages = [
    {
        "id": "efadb781-9b04-4aad-9afe-e79faef8cffb",
        "sent_at": datetime.datetime(2022, 10, 11, 23, 11, 11, 721),
        "sent_by": 46,  # id пользователя-отправителя
        "reply_for": "7b22ae19-6c58-443e-b138-e22784878581",  # id сообщение, на которое это сообщение является ответом (может быть None)
        "seen_by": [26, 91, 71], # идентификаторы пользователей, которые видели это сообщение
        "text": "А когда ревью будет?",
    }
]

#print ("Вывести айди пользователя, который написал больше всех сообщений.")

message_counts = Counter(message ['sent_by'] for message in messages)
# Находим пользователя с максимальным количеством сообщений
most_active_user_id = max(message_counts, key=message_counts.get)

print(f"Пользователь {most_active_user_id} написал больше всех сообщений: {message_counts[most_active_user_id]}")


#print ("Вывести айди пользователя, на сообщения которого больше всего отвечали.")
message_counts_reply = Counter(message ['reply_for'] for message in messages)
# Находим пользователя, на сообщения которого больше всего отвечалиий
most_active_user_id1 = max(message_counts_reply, key=message_counts.get)

print(f"Пользователь {most_active_user_id1} на сообщения которого больше всего отвечали: {message_counts_reply[most_active_user_id1]}")


# 3. Создаем словарь, в котором будем хранить количество уникальных пользователей, которые видели каждое сообщение
seen_counts = {}

# Проходимся по всем сообщениям
for message in messages:
    # Считаем количество уникальных пользователей, которые видели это сообщение
    seen_by = set(message["seen_by"])
    seen_count = len(seen_by)
    
    # Обновляем словарь seen_counts
    message_id = message["id"]
    seen_counts[message_id] = seen_count

# Находим сообщение с наибольшим количеством уникальных пользователей
max_seen_count = max(seen_counts.values())
max_seen_message_id = [k for k, v in seen_counts.items() if v == max_seen_count][0]

# Выводим идентификаторы пользователей, которые видели это сообщение
max_seen_message = next(message for message in messages if message["id"] == max_seen_message_id)
seen_by = max_seen_message["seen_by"]
print(f"ID пользователей, которые видели это сообщение: {seen_by}" )



# 4. Создаем словарь, в котором будем хранить количество сообщений, отправленных в каждый период
message_counts = {"morning": 0, "day": 0, "evening": 0}

# Проходимся по всем сообщениям
for message in messages:
    # Получаем время отправки сообщения
    sent_at = message["sent_at"]
    hour = sent_at.hour
    
    # Определяем, в какой период попадает время отправки сообщения
    if hour < 12:
        period = "morning"
    elif hour < 18:
        period = "day"
    else:
        period = "evening"
    
    # Увеличиваем счетчик сообщений для соответствующего периода
    message_counts[period] += 1

# Находим период, в котором было отправлено больше всего сообщений
max_count = max(message_counts.values())
max_period = [k for k, v in message_counts.items() if v == max_count][0]

# Выводим результат
print("Больше всего сообщений было отправлено в", max_period)


# 5.Создаем словарь, в котором будем хранить длины цепочек ответов для каждого сообщения
thread_lengths = {}

# Проходимся по всем сообщениям
for message in messages:
    # Получаем идентификатор сообщения и сообщение, на которое оно ответило
    message_id = message["id"]
    reply_for = message["reply_for"]

    if reply_for in thread_lengths:
    # Если сообщение является ответом на другое сообщение, то его длина цепочки ответов равна длине цепочки ответов родительского сообщения плюс 1
        thread_lengths[message_id] = thread_lengths.get(reply_for) + 1
    else:
        thread_lengths[message_id] = 1
    

# Находим несколько сообщений с наибольшей длиной цепочки ответов
max_threads = sorted(thread_lengths.items(), key=lambda x: x[1], reverse=True)[:5]

# Выводим идентификаторы сообщений, которые стали началом для самых длинных тредов
print("ID, которые стали началом для самых длинных тредов:")
for message_id, thread_length in max_threads:
    print(message_id)