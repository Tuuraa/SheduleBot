import bs4
import requests
import os


def get_full_fac(indexValue, fac: str):
    req = requests.get("https://elkaf.kubstu.ru/timetable/default/time-table-student-ofo?iskiosk=0&fak_id="+fac+"&kurs=1&gr=&ugod=2022&semestr=1", verify=False)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')

    data = str(soup.find_all("option")).split("</option>")

    _all = []
    facults = [[], []]

    for i in data:
        now_facult = str(i)
        index = now_facult.find(">")
        _all.append(now_facult[index + 1:])

    for i in _all:
        if "Институт" in i:
            facults[0].append(i)
        if str(i[:2]).isdigit() and len(i) > 1:
            facults[1].append(i)

    return facults[indexValue]

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
kurs = [i for i in range(1, 7)]
fac = ['495', '516', '490', '29', '538', '539', '540']

facults = get_full_fac(0, '495')
number = 0

for item in fac:
    os.mkdir(str(facults[number]))
    groups = get_full_fac(1, str(item))

    for group in groups:
        for i in range(1, 7):
            req = requests.get("https://elkaf.kubstu.ru/timetable/default/time-table-student-ofo?iskiosk=0&fak_id=516&kurs=1&gr=22-%D0%9A%D0%91-%D0%9F%D0%982&ugod=2022&semestr=1", verify=False)
            response = bs4.BeautifulSoup(req.text, 'lxml')
            schedules = response.find_all('div', class_="col-md-6 ned-box")
            for sch in schedules:
                schedule = bs4.BeautifulSoup(str(sch), 'html.parser')
                data = schedule.find_all('p')
                count = 5
                for temp in data[1:]:
                    count += 1
                    
                    print(temp.text)

            break
        break
    break
    number += 1



