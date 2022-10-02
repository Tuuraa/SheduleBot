from telebot import types
from Buttons import Buttons


def get_start_board():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🎓 Выбрать институт")
    btn2 = types.KeyboardButton("❓ Связаться с поддержкой")
    bt2 = types.KeyboardButton("📚 Мои расписания")
    markup.add().row(btn1, bt2)
    markup.add(btn2)

    return markup


def get_kurses_of_facult_for_back():
    result = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    result.add().row(types.KeyboardButton('1'),
                     types.KeyboardButton('2'),
                     types.KeyboardButton('3'))

    result.add().row(types.KeyboardButton('4'),
                     types.KeyboardButton('5'),
                     types.KeyboardButton('6'))

    result.add().row(Buttons.back, Buttons.back_facult)
    return result


def get_number_of_week_schedule_for_group_for_back():
    result = types.ReplyKeyboardMarkup(True, False)

    result.add().row(types.KeyboardButton("Четная неделя"), types.KeyboardButton("Нечетная неделя"))
    result.add(Buttons.back)
    result.add().row(Buttons.back_groups, Buttons.back_facult)
    return result


def get_markup_table(isSchedule=True):
    result = types.ReplyKeyboardMarkup(resize_keyboard=True)

    result.add(Buttons.back)
    if isSchedule:
        result.add().row(Buttons.back_groups, Buttons.back_kurse, Buttons.back_facult)

    return result


def get_start_for_person_schedule():
    result = types.ReplyKeyboardMarkup(resize_keyboard=True)
    result.add().row(
    types.KeyboardButton("Сегодня"),
    types.KeyboardButton("Завтра"),
    types.KeyboardButton("Потом"))
    result.add(Buttons.back)

    return result