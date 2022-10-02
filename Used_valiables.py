import os

facults = []
for filename in os.listdir("Институты"):
    facults.append(str(filename))

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
days_for_makson = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
weeks = ["Четная неделя", "Нечетная неделя"]
days_for_schedule = ["Сегодня", "Завтра", "Потом"]