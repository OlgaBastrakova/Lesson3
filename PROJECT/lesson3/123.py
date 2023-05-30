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


1. Вывести айди пользователя, который написал больше всех сообщений.
2. Вывести айди пользователя, на сообщения которого больше всего отвечали.
3. Вывести айди пользователей, сообщения которых видело больше всего уникальных пользователей.
4. Определить, когда в чате больше всего сообщений: утром (до 12 часов), днём (12-18 часов) или вечером (после 18 часов).
5. Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).

Весь код стоит разбить на логические части с помощью функций.
"""

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
import random
import uuid
import datetime
from typing import List, Dict, Any
import lorem
from collections import Counter

message_counts = Counter(messages ['sent_by'] for message in messages)
# Находим пользователя с максимальным количеством сообщений
most_active_user_id = max(message_counts, key=message_counts.get)

print(f"Пользователь {most_active_user_id} написал больше всех сообщений: {message_counts[most_active_user_id]}")


#Генерирует историю чата с заданным количеством сообщений.
def get_user_with_most_replies(messages: List[Dict[str, Any]]) -> int:
    """
    Возвращает идентификатор пользователя, на сообщения которого больше всего отвечали.

    :param messages: список сообщений
    :return: идентификатор пользователя
    """
    user_reply_count = {}
    for message in messages:
        reply_for = message["reply_for"]
        if reply_for is not None:
            user_id = messages[0]["sent_by"]
            if user_id not in user_reply_count:
                user_reply_count[user_id] = 0
            user_reply_count[user_id] += 1
    return max(user_reply_count, key=user_reply_count.get)


def get_users_with_most_views(messages: List[Dict[str, Any]]) -> List[int]:
    """
    Возвращает список идентификаторов пользователей, сообщения которых видело больше всего уникальных пользователей.

    :param messages: список сообщений
    :return: список идентификаторов пользователей
    """
    user_view_count = {}
    for message in messages:
        seen_by = message["seen_by"]
        for user_id in seen_by:
            if user_id not in user_view_count:
                user_view_count[user_id] = 0
            user_view_count[user_id] += 1
    max_views = max(user_view_count.values())
    return [user_id for user_id, views in user_view_count.items() if views == max_views]


def get_message_count_by_time_of_day(messages: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Возвращает словарь с количеством сообщений в разное время дня.

    :param messages: список сообщений
    :return: словарь с количеством сообщений в разное время дня
    """
    message_count_by_time = {"утром": 0, "днём": 0, "вечером": 0}
    for message in messages:
        sent_time = message["sent_at"].time()
        if sent_time < datetime.time(12):
            message_count_by_time["утром"] += 1
        elif sent_time < datetime.time(18):
            message_count_by_time["днём"] += 1
        else:
            message_count_by_time["вечером"] += 1
    return message_count_by_time


