from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

button_top = KeyboardButton("ТОП 🔝")
button_back = KeyboardButton("Назад")
button_profile = KeyboardButton("Профиль 👥")
button_notifications = KeyboardButton("Уведомления 🔔")
button_achievements = KeyboardButton("Достижения")

inlinebutton_1 = InlineKeyboardButton("Планка 10 минут", callback_data="b1")
inlinebutton_2 = InlineKeyboardButton("Зарядка", callback_data="b2")
inlinebutton_3 = InlineKeyboardButton("Растяжка", callback_data="b3")
inlinebutton_4 = InlineKeyboardButton("Интро", callback_data="b3")

achivment1=InlineKeyboardButton("Ленивец", callback_data="a1")
achivment2=InlineKeyboardButton("Гигачад", callback_data="a2")
achivment3=InlineKeyboardButton("Взломщик", callback_data="a3")
achivment4=InlineKeyboardButton("Шутник", callback_data="a4")
achivment5=InlineKeyboardButton("Врунишка", callback_data="a5")
achivment6=InlineKeyboardButton("Не дождётесь!", callback_data="a6") # стань топ 3 2 раза
achivment7 = InlineKeyboardButton("Конец?", callback_data="a7") # завершить челлендж
achivment8=InlineKeyboardButton("Вернуть отправителю", callback_data="a8") # ответить боту
achivment9=InlineKeyboardButton("А они меня ждут? Эти неприятности?", callback_data="a9") # начать челендж
achivment10=InlineKeyboardButton("Ветеран", callback_data="a10") # выполнять челендж 70 дней
achivment11=InlineKeyboardButton("Любопытной Варваре...", callback_data="a11") # нажать все кнопки
achivment12=InlineKeyboardButton("Ну-ка сделай!", callback_data="a12") # реализовать получение достижений пользователем

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True)
main_kb.row(button_profile, button_top)

profile_kb = ReplyKeyboardMarkup(resize_keyboard=True)
profile_kb.row(button_notifications, button_achievements, button_back)

inline_kb = InlineKeyboardMarkup().add(achivment9).add(achivment8).add(achivment11).row(achivment3, achivment1, achivment5)
inline_kb.row(achivment4, achivment6, achivment2).row(achivment10, achivment7, achivment12)