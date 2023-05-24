print("hello")
from datetime import datetime, timedelta
today = datetime.today()
print("Сегодня:", today.strftime('%A %D %B %Y'))
yesterday = today - timedelta(days=1)
print("Вчера:", yesterday.strftime('%A %D %B %Y'))
thirty_days_back = today - timedelta(days=30)
print("30 дней назад:", thirty_days_back.strftime('%A %D %B %Y'))
#dt_now = datetime.now()
#print(dt_now)



# Строка с датой и временем
date_string = "01/01/25 12:10:03.234567"

# Преобразование строки в объект datetime
date_object = datetime.strptime(date_string, '%d/%m/%y %H:%M:%S.%f')

print(date_object)