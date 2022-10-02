from telebot import types
import os

# Buttons
back = types.KeyboardButton("⬅ Вернуться к началу")
back_facult = types.KeyboardButton("⬅ Вернуться к факультетам")
back_kurse = types.KeyboardButton("⬅ Вернуться к курсу")
back_groups = types.KeyboardButton("⬅ Вернуться к группам")
back_weeks = types.KeyboardButton("⬅ Вернуться к неделям")

# variables used
facult_name = ""
kurs = ""
group = ""
number_week = ""
day_of_week = ""

# variables used
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
weeks = ["Четная неделя", "Нечетная неделя"]
groups = []
gors = {}
groups_for_gors = []
id_list = []
view_schedule = False
check_veiw = False
group_for_schedule_today = ""

# used txt files
facults = []
for filename in os.listdir("Институты"):
    facults.append(str(filename))


def get_start_board():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🎓 Выбрать институт")
    btn2 = types.KeyboardButton("❓ Связаться с поддержкой")
    bt2 = types.KeyboardButton("📚 Мои расписания")
    markup.add().row(btn1, bt2)
    markup.add(btn2)

    global now_markup
    now_markup = markup

    return markup


def get_all_inst(check=False):

    if check:
        global view_schedule
        view_schedule = True

    buttons = [types.KeyboardButton(i) for i in facults]
    result = types.ReplyKeyboardMarkup(True)

    result.add().row(buttons[0], buttons[1])
    result.add().row(buttons[2], buttons[3], buttons[4])
    result.add().row(buttons[5], buttons[6])

    result.add(back)

    return result


def get_groups_of_facult(kurs_mes):
    global kurs
    kurs = kurs_mes

    global groups
    groups = []

    for i in os.listdir(path + '\\' + facult_name + '\\' + kurs):
        groups.append(i)

    buttons = [types.KeyboardButton(i) for i in groups]
    result = types.ReplyKeyboardMarkup(resize_keyboard=False)

    for but in buttons:
        result.add(but)
    result.add().row(back, back_kurse, back_facult)

    return result



def get_number_of_week_schedule_for_group(mess, isShedule=True):

    global group
    group = mess

    result = types.ReplyKeyboardMarkup(resize_keyboard=True)

    result.add().row(types.KeyboardButton("Четная неделя"), types.KeyboardButton("Нечетная неделя"))
    result.add(back)
    if isShedule:
        result.add().row(back_groups, back_facult)

    return result


def get_day_of_week_schedule_for_group(day, isShedule=True):

    global number_week
    number_week = day

    result = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for i in range(len(days) - 1):
        result.add(types.KeyboardButton(days[i]))

    result.add(back)
    if isShedule:
        result.add().row(back_weeks, back_kurse)
        result.add().row(back_groups, back_facult)

    return result


def get_number_of_week_schedule_for_group_for_back():
    result = types.ReplyKeyboardMarkup(True, False)

    result.add().row(types.KeyboardButton("Четная неделя"), types.KeyboardButton("Нечетная неделя"))
    result.add(back)
    result.add().row(back_groups, back_facult)

    return result


def get_markup_table(isSchedule=True):
    result = types.ReplyKeyboardMarkup(resize_keyboard=True)

    result.add(back)
    if isSchedule:
        result.add().row(back_groups, back_kurse, back_facult)

    return result


def get_my_schedule(id):

    result = types.ReplyKeyboardMarkup(resize_keyboard=True)

    id_list = []

    for i in os.listdir("Расписания пользователей"):
        id_list.append(i[:-4])

    if str(id) in id_list:
        try:
            with open("Расписания пользователей\\" + str(id) + '.txt', 'r', encoding='utf8') as file:
                local_groups = list(file.read().split('\n'))

            global gors, groups_for_gors
            gors = {}
            groups_for_gors = []
            count = 0

            for i in local_groups:
                if len(i) != 0:
                    g = list(i.split('\\'))
                    gors[count] = [g[0], g[1], g[2]]
                    count += 1

            for i in gors.values():
                groups_for_gors.append(i[2])
                result.add(types.KeyboardButton(str(i[2])))

        except:
            pass

    result.add().row(back, types.KeyboardButton("Добавить расписание"))

    return result


def get_start_for_person_schedule():
    result = types.ReplyKeyboardMarkup(resize_keyboard=True)
    result.add().row(
    types.KeyboardButton("Сегодня"),
    types.KeyboardButton("Завтра"),
    types.KeyboardButton("Потом"))
    result.add(back)

    return result