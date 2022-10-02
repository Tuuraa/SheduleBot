import telebot
import Markups
import datetime
import PersonsList
import Used_valiables
from markups_obj import Person
import Common_markups


Token = "5656238548:AAGjSpVQVoYdtFZ8XelLzFEBjqTBkhI7ask"
bot = telebot.TeleBot(token=Token)

list_id_persons = []
now_person = Person(12, "any")

@bot.message_handler(commands=["start"])
def start(message):
    print(message.text)
    check = False
    for i in list_id_persons:
        if i.id_person == message.chat.id:
            global now_person
            now_person = i
            check = True
            break

    if not check:
        new_person = Person(message.chat.id, message.text)
        list_id_persons.append(new_person)
        now_person = new_person

    bot.send_message(message.chat.id,
            text="Привет, {0.first_name}! Я тестовый бот для расписания в Вузе КубГТУ".format(message.from_user),
            reply_markup=Common_markups.get_start_board())


@bot.message_handler(func=lambda message: (message.text in now_person.groups_for_gors
                                          or message.text in Used_valiables.days_for_schedule
                                          or message.text in Used_valiables.days
                                          or message.text in Used_valiables.weeks)
                                          and not now_person.check_add_schedule
                                          and not now_person.view_schedule)

def get_schedule(message):

    if message.text in now_person.groups_for_gors:
            now_person.group_for_schedule_today = message.text
            bot.send_message(message.chat.id, "Выберите на когда вам нужно расписание", reply_markup=Common_markups.get_start_for_person_schedule())

    elif message.text == "Сегодня":
            week = int(datetime.datetime.utcnow().isocalendar()[1])
            x = "Четная неделя" if week % 2 == 0 else "Нечетная неделя"
            day = int(datetime.datetime.utcnow().isocalendar()[2])
            bot.send_message(message.chat.id,
                             now_person.get_schedule_for_group("", group_for_check=now_person.group_for_schedule_today, dateToday=Used_valiables.days[day-1], isScheduleToday=True, num_week=x),
                             reply_markup=Common_markups.get_start_for_person_schedule())

    elif message.text == "Завтра":
            day_numb = datetime.datetime.weekday(datetime.datetime.now()) % 6
            day = int(datetime.datetime.utcnow().isocalendar()[2]) % 6
            week = int(datetime.datetime.utcnow().isocalendar()[1])
            x = "Четная неделя" if week % 2 == 0 else "Нечетная неделя"
            bot.send_message(message.chat.id,
                             now_person.get_schedule_for_group("", group_for_check=now_person.group_for_schedule_today, dateToday=Used_valiables.days[day], isScheduleToday=True, num_week=x),
                             reply_markup=Common_markups.get_start_for_person_schedule())

    elif message.text == "Потом":
            week = int(datetime.datetime.utcnow().isocalendar()[1])
            x = "Четная неделя" if week % 2 == 0 else "Нечетная неделя"
            bot.send_message(message.chat.id, "Неделю", reply_markup=now_person.get_even_number_of_week(message.text, isShedule=False))
            bot.send_message(message.chat.id, f"Сейчас {x.lower()}")

    elif str(message.text) in Markups.weeks:
            bot.send_message(message.chat.id, "Дни", reply_markup=now_person.get_day_of_week(message.text, isShedule=False))

    elif str(message.text) in Markups.days:
            bot.send_message(message.chat.id,
                             now_person.get_schedule_for_group("", group_for_check=now_person.group_for_schedule_today,
                                                            dateToday=message.text, isScheduleToday=True,
                                                            num_week=now_person.number_week),
                                                            reply_markup=now_person.get_day_of_week(now_person.number_week, isShedule=False))

@bot.message_handler(func=lambda message: (message.text in PersonsList.list_message
                                          or message.text in Used_valiables.facults
                                          or message.text in now_person.groups
                                          or str(message.text).isdigit()
                                          or message.text in PersonsList.sure)
                                          and now_person.check_add_schedule
                                          and not now_person.view_schedule)

def login(message):

    if not now_person.check_add_schedule:
        func(message)

    elif message.text in Markups.facults:
            now_person.facult_name_for_add = message.text
            bot.send_message(message.chat.id,
                             PersonsList.list_message[1], reply_markup=now_person.get_kurses_of_facult(message.text))

    elif str(message.text).isdigit():
            now_person.kurs_for_add = message.text
            bot.send_message(message.chat.id,
                             PersonsList.list_message[2], reply_markup=now_person.get_groups_of_facult(message.text))

    elif message.text in now_person.groups:
            now_person.group_for_add = message.text
            bot.send_message(message.chat.id,
                             PersonsList.list_message[3], reply_markup=PersonsList.add_sure())

    elif message.text in PersonsList.sure:
        bot.send_message(message.chat.id, now_person.get_new_personal_schedule(message.chat.id), reply_markup=Common_markups.get_markup_table(False))


@bot.message_handler(content_types=['text'])
def func(message):

    print(message.text)
    check = False
    for i in list_id_persons:
        if i.id_person == message.chat.id:
            global now_person
            now_person = i
            check = True
            break

    if not check:
        new_person = Person(message.chat.id, message.text)
        list_id_persons.append(new_person)
        now_person = new_person

    if message.text == "🎓 Выбрать институт":
        now_person.view_schedule = True
        mes = now_person.get_all_facults(True)
        bot.send_message(message.chat.id, "Все институты", reply_markup=mes)

    elif message.text == "❓ Связаться с поддержкой":
        #bot.send_message(message.chat.id, "Номер разработчика")
        bot.send_message(message.chat.id, "Данный бот находится в разработке,на данный момент нет поддержки")
        #bot.send_contact(message.chat.id, "+79897898328", "Artur", "Kardanov")

    elif message.text in Used_valiables.facults:
        bot.send_message(message.chat.id, "Курсы", reply_markup=now_person.get_kurses_of_facult(message.text))

    elif message.text in now_person.groups:
        bot.send_message(message.chat.id, "Четная или нечетная неделя", reply_markup=now_person.get_even_number_of_week(message.text))
        week = int(datetime.datetime.utcnow().isocalendar()[1])
        x = "Четная неделя" if week % 2 == 0 else "Нечетная неделя"
        bot.send_message(message.chat.id, f"Сейчас {x.lower()}")

    elif message.text == "📚 Мои расписания":
        now_person.check_veiw = True
        bot.send_message(message.chat.id, "Мои расписания",
                     reply_markup=now_person.get_my_schedule(message.chat.id))

    elif message.text == "Добавить расписание":
        now_person.check_add_schedule = True
        bot.send_message(message.chat.id, "Добавление института", reply_markup=Markups.get_all_inst())

    elif str(message.text).isdigit():
        bot.send_message(message.chat.id, "Группы", reply_markup=now_person.get_groups_of_facult(message.text))

    elif str(message.text) in Used_valiables.weeks:
        bot.send_message(message.chat.id, "Дни", reply_markup=now_person.get_day_of_week(message.text))

    elif str(message.text) in Used_valiables.days:
        bot.send_message(message.chat.id, now_person.get_schedule_for_group(message.text))
        bot.send_message(message.chat.id, "", reply_markup=Common_markups.get_markup_table())

    elif message.text == "⬅ Вернуться к группам":
        bot.send_message(message.chat.id, "Вернулся к группам", reply_markup=now_person.remove_groups())

    elif message.text == "⬅ Вернуться к неделям":
        bot.send_message(message.chat.id, "Вернулся к неделе", reply_markup=Common_markups.get_number_of_week_schedule_for_group_for_back())

    elif message.text == "⬅ Вернуться к курсу":
        bot.send_message(message.chat.id, "Вернулся к курсам", reply_markup=Common_markups.get_kurses_of_facult_for_back())

    elif message.text == "⬅ Вернуться к факультетам":
        bot.send_message(message.chat.id, "Вернулся к факультетам", reply_markup=now_person.get_all_facults())

    elif message.text == "⬅ Вернуться к началу":
        now_person.view_schedule = False
        now_person.check_veiw = False
        past = Common_markups.get_start_board()
        bot.send_message(message.chat.id, "Вернулся к началу", reply_markup=past)


bot.polling(none_stop=True, interval=0)
