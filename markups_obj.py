from telebot import types
import os
import Used_valiables
from Buttons import Buttons


class Person:

    def __init__(self, id, name):

        #Уникальный id пользователя и его имя
        self.id_person = id
        self.name_person = name

        #Переменные для нахождения расписания
        self.facult_name = ""
        self.kurs = ""
        self.group = ""
        self.number_week = ""
        self.day_of_week = ""

        #Флаги для определения обработчика сообщений
        self.view_schedule = False
        self.check_veiw = False

        #Остальные придаточные переменные для определения расписания пользователя
        self.groups = []
        self.gors = {}
        self.groups_for_gors = []
        self.id_list = []
        self.group_for_schedule_today = ""

        #Переменные для добавления нового расписания пользователю
        self.check_add_schedule = False
        self.facult_name_for_add = ""
        self.kurs_for_add = ""
        self.group_for_add = ""

    def get_all_facults(self, check=False):

        if check:
            self.view_schedule = True

        buttons = [types.KeyboardButton(i) for i in Used_valiables.facults]
        result = types.ReplyKeyboardMarkup(True)

        result.add().row(buttons[0], buttons[1])
        result.add().row(buttons[2], buttons[3], buttons[4])
        result.add().row(buttons[5], buttons[6])

        result.add(Buttons.back)

        return result


    def get_groups_of_facult(self, kurs_mes):
        self.kurs = kurs_mes
        self.groups = []

        for i in os.listdir("Институты" + '/' + self.facult_name + '/' + self.kurs):
            self.groups.append(i)

        buttons = [types.KeyboardButton(i) for i in self.groups]
        result = types.ReplyKeyboardMarkup(resize_keyboard=False)

        for but in buttons:
            result.add(but)
        result.add().row(Buttons.back, Buttons.back_kurse, Buttons.back_facult)
        return result


    def get_kurses_of_facult(self, fac):
        self.facult_name = fac
        self.groups = []

        result = types.ReplyKeyboardMarkup(resize_keyboard=True)

        result.add().row(types.KeyboardButton('1'),
                types.KeyboardButton('2'),
                types.KeyboardButton('3'))

        result.add().row(types.KeyboardButton('4'),
                types.KeyboardButton('5'),
                types.KeyboardButton('6'))

        result.add().row(Buttons.back, Buttons.back_facult)
        return result


    def get_even_number_of_week(self, mess, isShedule=True):
        self.group = mess
        result = types.ReplyKeyboardMarkup(resize_keyboard=True)

        result.add().row(types.KeyboardButton("Четная неделя"), types.KeyboardButton("Нечетная неделя"))
        result.add(Buttons.back)
        if isShedule:
            result.add().row(Buttons.back_groups, Buttons.back_facult)

        return result


    def get_day_of_week(self, day, isShedule=True):
        self.number_week = day

        result = types.ReplyKeyboardMarkup(resize_keyboard=True)
        days = Used_valiables.days

        for i in range(len(days) - 1):
            result.add(types.KeyboardButton(days[i]))

        result.add(Buttons.back)
        if isShedule:
            result.add().row(Buttons.back_weeks, Buttons.back_kurse)
            result.add().row(Buttons.back_groups, Buttons.back_facult)
        return result


    def remove_groups(self):
        self.groups = []

        for i in os.listdir("Институты" + '\\' + self.facult_name + '\\' + self.kurs):
            self.groups.append(i)

        buttons = [types.KeyboardButton(i) for i in self.groups]
        result = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for but in buttons:
            result.add(but)
        result.add(Buttons.back)
        result.add().row(Buttons.back_kurse, Buttons.back_facult)
        return result


    def get_schedule_for_group(self, day_item, group_for_check=None, dateToday= None, isScheduleToday= False, num_week=None):

        if isScheduleToday:
            try:
                if len(self.groups_for_gors) == 0:
                    return "Перезапустите бота /start"

                index = 0
                for i in self.groups_for_gors:
                    if group_for_check == i:
                        break
                    else:
                        index += 1

                self.facult_name = self.gors[index][0]
                self.kurs = self.gors[index][1]
                self.group = self.gors[index][2]
                self.number_week = num_week
                day_item = dateToday

            except:
                return "Перезапустите бота /start"
        if (self.facult_name and self.kurs and self.group and self.number_week and day_item) != "":

            try:
                path_schedule = "Институты" + '\\' + self.facult_name + '\\' + self.kurs + '\\' + self.group + '\\' + self.number_week + '\\' + day_item + '.txt'
                with open(path_schedule) as file:
                    scheduleText = file.read()
            except:
                scheduleText = "Нет пар"

            return scheduleText
        else:
            return "Перезапустите бота /start"


    def get_my_schedule(self, id):

        result = types.ReplyKeyboardMarkup(resize_keyboard=True)

        id_list = []

        for i in os.listdir("Расписания пользователей"):
            id_list.append(i[:-4])

        if str(id) in id_list:
            try:
                with open("Расписания пользователей\\" + str(id) + '.txt', 'r', encoding='utf8') as file:
                    local_groups = list(file.read().split('\n'))

                self.gors = {}
                self.groups_for_gors = []
                count = 0

                for i in local_groups:
                    if len(i) != 0:
                        g = list(i.split('\\'))
                        self.gors[count] = [g[0], g[1], g[2]]
                        count += 1

                for i in self.gors.values():
                    self.groups_for_gors.append(i[2])
                    result.add(types.KeyboardButton(str(i[2])))

            except:
                pass

        result.add().row(Buttons.back, types.KeyboardButton("Добавить расписание"))
        return result

    def get_new_personal_schedule(self, id):

        self.check_add_schedule = False
        if self.facult_name_for_add == "" or self.kurs_for_add == "" or self.group_for_add == "":
            return "Перезапустите бота"

        try:
            list_shed = []
            with open("Расписания пользователей\\" + f'{id}.txt', 'r', encoding='utf8') as file:
                list_shed = file.read().split('\n')

            if f"{self.facult_name_for_add}\\{self.kurs_for_add}\\{self.group_for_add}" in list_shed:
                return "Эта группа уже в вашем расписании"

            list_shed.append(f"{self.facult_name_for_add}\\{self.kurs_for_add}\\{self.group_for_add}")

            with open("Расписания пользователей\\" + f'{id}.txt', 'w', encoding='utf8') as file:
                for i in list_shed:
                    file.write(i + '\n')

        except:
            try:
                with open("Расписания пользователей\\" + f'{id}.txt', 'w+', encoding='utf8') as file:
                    file.write('\n')
                    file.write(f"{self.facult_name_for_add}\\{self.kurs_for_add}\\{self.group_for_add}")
            except:
                return "Ошибка"

        return "Расписание добавлено"
