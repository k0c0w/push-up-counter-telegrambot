
import database
import keyboards
from  notifier import Notifier
from telebot import  types
import telebot

from datetime import datetime
import dayscalculater
AIM = 10000
DaysLeft = dayscalculater.DaysLeft
#DaysLeft = (datetime(day=1, month= 9, year= 2022) - datetime.now()).days

Token = "TOKEN"

#сам бот
bot = telebot.TeleBot(token=Token)

@bot.callback_query_handler(func = lambda c: c.data.startswith('a'))
def process(callback_query: types.CallbackQuery):
    code = int(callback_query.data[1:])
    if code == 1:
        m = "💤\nНе отжиматься 2 дня и более."
        show_alert(m,callback_query)
    elif code == 2:
        m = "🚗\nПревысить отметку в 5000 отжиманий."
        show_alert(m, callback_query)
    elif code == 3:
        m = "🤦\nПослать некорректное выражение более 5 раз"
        show_alert(m, callback_query)
    elif code == 4:
        m = "😂\nРассказать анекдот или сделать 300 отжиманий за раз."
        show_alert(m, callback_query)
    elif code == 5:
        m = "🙊\nПрислать не реалистичное количество отжиманий."
        show_alert(m, callback_query)
    elif code == 6:
        m = "🔥\nЗанять топ 3 более 1 раза."
        show_alert(m, callback_query)
    elif code == 7:
        m = "🎉🎉🎉\nУспешно завершить челлендж!"
        show_alert(m, callback_query)
    elif code == 8:
        m = "Отправить ответ на сообщение бота"
        show_alert(m, callback_query)
    elif code == 9:
        m = "😅\nНужно ли начинать челлендж?"
        show_alert(m, callback_query)
    elif code == 10:
        m = "Принимать участие в челлендже более 70 дней и иметь более 3000 отжиманий"
        show_alert(m, callback_query)
    elif code == 11:
        m = "⁉\nНажать все кнопки"
        show_alert(m, callback_query)
    elif code == 12:
        m = "Реализовать получение достижений username"
        show_alert(m, callback_query)
    else:
        bot.callback_query_handler(callback_query.id)


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    user_id = message.from_user.id
    if message.from_user.last_name:
        last = message.from_user.last_name[:1]
    try:
        name = f"{message.from_user.first_name} {last}."
    except:
        name = "Не опознан"
    bot.send_message(user_id,"Делай отжимания и присылай мне количество, а я буду их считать!\nНе забывай про растяжку!\nhttps://youtube.com/shorts/ba8tr1NzwXU?feature=share",
                         reply_markup=keyboards.main_kb)
    database.updatebase(user_id, name)


@bot.message_handler(content_types=['text'])
def messages(message: types.Message):
    text = message.text
    if str.isdigit(text):
        pushupsCounter(message, int(text))
    elif text == "ТОП 🔝":
        replyTop(message)

    elif text == "Профиль 👥":
        bot.send_message(message.from_user.id,"<", reply_markup= keyboards.profile_kb)
        bot.delete_message(message.from_user.id,message_id=message.id)
    elif text == "Уведомления 🔔":
        switch_notifications_mode(message)
    elif text == "Достижения":
        bot.send_message(message.from_user.id, "Я ленивый бот, поэтому выдавай достижения сам!\nТолько честно! ;)", reply_markup=keyboards.inline_kb)
        bot.delete_message(message.from_user.id, message_id=message.id)
    elif text == "Назад":
        bot.send_message(message.from_user.id,text=">",reply_markup= keyboards.main_kb)
        bot.delete_message(message.from_user.id, message_id=message.id)
    else:
        bot.send_message(message.from_user.id, "Я не ИИ. Введи корректное число!")

def show_alert(message: str, callback):
    bot.answer_callback_query(callback.id, text=message, show_alert=True)

def switch_notifications_mode(message: types.Message):
    us_id = message.from_user.id
    new_permission = database.switch_notifications(us_id)
    if new_permission:
        bot.send_message(us_id,text="Уведомления включены.", reply_markup=keyboards.profile_kb)
    else:
        bot.send_message(us_id,text= "Уведомления выключены.", reply_markup=keyboards.profile_kb)


def replyTop(message: types.Message):
    toplist = database.get_top()
    userResult = database.get_user_result(message.from_user.id)
    answer = "Топ 3:\n"
    place = 1
    for tuple in toplist:
        answer +=f"{place}. {tuple[0]}: {tuple[1]}\n"
        place += 1
    bot.send_message(message.from_user.id, text=answer + f"\nВаш результат: {userResult}", reply_markup= keyboards.main_kb)
    bot.delete_message(message.from_user.id, message_id=message.id)

def pushupsCounter(message: types.Message,count: int):
    us_id = message.from_user.id
    if count <= 0:
        bot.send_message(us_id,"Обратные отжимания? :D")
        return
    doneInfo = database.getPushupsCount(message.from_user.id)
    if doneInfo is None:
        # TODO: выдать достижение взломщик
        bot.send_message(us_id,"Упс! Ты что-то сломал. :D")
        return
    totaldone = doneInfo[0] + count
    doneperday = doneInfo[1] + count
    if totaldone >= AIM:
        bot.send_message(us_id,"Красава харэ онжуматься иди подтягиваться! 🗿")
        return
    database.update_pushups(message.from_user.id, totaldone, doneperday)

    bot.send_message(us_id, text = toDo(doneperday,doneInfo[2], totaldone))

from  random import choice
def toDo(done:int, aim: int, total: int):
    variants =["💪 Молодец!", "🔥 Продолжай!", "😎 Чел, харош!"]
    addition = ""
    if(done > aim):
        addition = "\nМожешь отдохнуть! Не забудь про растяжку!"
    return f"{choice(variants)} {total/AIM*100:.1f}%\nЦель на день: ☑ {done}/{aim}{addition}"


if __name__ == "__main__":
    database.init()
    database.update_users_aim()
    Notifier(target=bot).notify()
    bot.polling(none_stop=True)

