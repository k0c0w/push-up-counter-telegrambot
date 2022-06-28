from  telebot import TeleBot
import database

import keyboards

Message = "Ты не забыл про меня?🤔 Жду твоего отчета!"

class Notifier:

    def __init__(self, target: TeleBot):
        self.bot = target

    def notify(self):
        while True:
            baned = list()
            for user in database.get_users_for_mailing():
                try:
                    self.bot.send_message(user, Message, reply_markup= keyboards.main_kb)
                except Exception as e:
                    print(e)
                    baned.append(user)
            #TODO: вынести на части, вдруг окажется что список на 1 млн юзеров, озу не хватит
            if len(baned) > 0:
                database.remove_from_mailing(baned)
            break