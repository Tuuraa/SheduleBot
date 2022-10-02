from telebot import types
import Markups
import os

#messages for add new schedule
list_message = ["Добавление института", "Добавление курса", "Добавление группы", "Вы уверенны?"]

# persons schedule
check_add_schedule = False

# variables used
facult_name = ""
kurs = ""
group = ""

#
list_id_for_schedule = []
kurses = []
groups = []
sure = ["Да", "Нет"]

#

def add_sure():
    result = types.ReplyKeyboardMarkup(resize_keyboard=True)
    result.add().row(types.KeyboardButton(sure[0]), types.KeyboardButton(sure[1]))

    result.add().row(Markups.back, Markups.back_groups)
    result.add().row(Markups.back_kurse, Markups.back_facult)

    return result
