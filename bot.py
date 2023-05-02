# -*- coding: utf-8 -*-

import telebot
from telebot import types
import config
from dilevery import text_post
from PIL import Image
import PIL

bot = telebot.TeleBot(config.TOKEN)

user_dict = {}
hello_count = []
input_message = []

class User:
    def __init__(self, name):
        self.name = name

@bot.message_handler(commands=['id'])
def process_id(message):
    bot.send_message(message.chat.id, "Твоій ID: " + str(message.from_user.id), parse_mode = 'HTML')

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if message.chat.id == config.my_id:

        key1 = types.ReplyKeyboardMarkup(True, False)
        key1.row("Перейти до створення постів")
        bot.send_message(message.chat.id,
                                     "Ти у головному меню".format(
                                         message.from_user, bot.get_me()),
                                     parse_mode='html', reply_markup=key1)
        if message.text == "Перейти до створення постів":
            key1 = types.ReplyKeyboardMarkup(True,False)
            key1.row("Створити оголошення")
            key1.row("Пост з прроцедурою доставки")
            bot.send_message(message.chat.id,
                                     "Вибери пункт!".format(
                                         message.from_user, bot.get_me()),
                                     parse_mode='html', reply_markup=key1)
        elif message.text == "Пост з прроцедурою доставки":
            dilevery(message.text)

        elif message.text == "Створити оголошення":
            bot.register_next_step_handler(message, process_name_step)
        else:
            pass
    else:
    	bot.send_message(message.chat.id, 'У вас немає доступу до даного бота')
    	bot.send_message(config.my_id,'Привіт, ' + str(message.from_user.first_name) + " хотів скористатись ботом, але я попередив його що з тобою не варто зв'язуватись 😎\nНижче я тобі переслав повідомлення, яке Він хотів написати.")
    	bot.forward_message(config.my_id, message.chat.id, message.message_id)
    	pass

def process_name_step(message):
    bot.send_message(message.chat.id, 'А тепер завантаж фото.')
    input_message.clear()
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    user_dict[chat_id] = user
    input_message.append(str(user.name))
    if message.text == "Пост з прроцедурою доставки":
        callback_delivery(message)
    elif message.text == "Меню":
        bot.send_message(message.chat.id, 'Входжу в главне меню')
        send_welcome(message)
    elif message.text == "Створити оголошення":
        bot.send_message(message.chat.id, "Неправильний текст, вибери потрібний пункт")
        pass

    else:
        statup(message)
        
        #bot.send_message(config.owner, user.name, reply_markup=markup, # Можна відправляти тільки текст без зображень для цього достатньо -
                #parse_mode="Markdown") № лише видалити або закоментувати функцію photo_handler
        
def dilevery(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("📲✍🏻 Зв'язок з менеджером", url='https://t.me/YuraBossAutoUkraine')
    item2 = types.InlineKeyboardButton("🔎🚗 Індивідуальний підбір авто", url = 'https://forms.gle/ynPfcTESRjfDdaiYA')
    item3 = types.InlineKeyboardButton("📞📟 Контакти на сайті", url = "https://bossautoukraine.com.ua/")

    markup.add(item1, item2, item3)
    bot.send_message(config.owner, text_post, reply_markup=markup,
           parse_mode="Markdown")
    bot.send_message(config.my_id, 'Пост з *процедурою доставки* опублікований!', parse_mode="Markdown")

@bot.message_handler(regexp = 'Меню')
def menu(message):
	if message.chat.id == config.my_id:
	    if message.text == "Меню": 
	        bot.send_message(message.chat.id, 'Входжу в главне меню')
	        send_welcome(message)
	    else:
	        statup(message)
	else:
		bot.send_message(message.chat.id, 'У вас немає доступу до даного бота')
		bot.send_message(config.my_id,'Привіт, ' + str(message.from_user.first_name) + " хотів скористатись ботом, але я попередив його що з тобою не варто зв'язуватись 😎\nНижче я тобі переслав повідомлення, яке Він хотів написати.")
		bot.forward_message(config.my_id, message.chat.id, message.message_id)
		pass

@bot.message_handler(content_types=['text', 'photo'])
def statup(message):
    if message.chat.id == config.my_id:
        if message.content_type == 'text':
            if message.chat.type == 'private':
                if message.text == "Пост з прроцедурою доставки":
                    callback_delivery(message)

                elif message.text == "Створити оголошення":
                    key1 = types.ReplyKeyboardMarkup(True, False)
                    key1.row("Меню")
                    bot.send_message(message.chat.id,
                                                 "Спочатку введи текст оголошення".format(
                                                     message.from_user, bot.get_me()),
                                                  parse_mode='html', reply_markup=key1)
                    bot.register_next_step_handler(message, process_name_step)

                elif message.text == "Меню":
                    send_welcome(message)

                if message.text == "Перейти до створення постів":
                    key1 = types.ReplyKeyboardMarkup(True,False)
                    key1.row("Створити оголошення")
                    key1.row("Пост з прроцедурою доставки")
                    bot.send_message(message.chat.id,
                                             "Вибери пункт!".format(
                                                 message.from_user, bot.get_me()),
                                             parse_mode='html', reply_markup=key1)

                else:
                    pass
        if message.content_type == 'photo':
            photo_handler(message)
    else:
    	bot.send_message(message.chat.id, 'У вас немає доступу до даного бота')
    	bot.send_message(config.my_id,'Привіт, ' + str(message.from_user.first_name) + " хотів скористатись ботом, але я попередив його що з тобою не варто зв'язуватись 😎\nНижче я тобі переслав повідомлення, яке Він хотів написати.")
    	bot.forward_message(config.my_id, message.chat.id, message.message_id)
    	pass

def photo_handler(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("👉 Зв'язок з менеджером👈", url='https://t.me/YuraBossAutoUkraine')
    markup.add(item1)
    key1 = types.ReplyKeyboardMarkup(True, False)
    key1.row("Меню")
    raw = message.photo[1].file_id
    name = raw+".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name,'wb') as new_file:
        new_file.write(downloaded_file)
    img = open(name, 'rb')
    bot.send_photo(config.owner, img, input_message, ''.format(
                                     message.from_user, bot.get_me()),
                                 parse_mode='html', reply_markup=markup)
    bot.send_message(message.chat.id, 'Повідомлення надіслано в групу, щоб продовжити, натисни *"Меню"*'.format(
                                         message.from_user, bot.get_me()),
                                     parse_mode='Markdown', reply_markup=key1)

def callback_delivery(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item4 = types.InlineKeyboardButton("ТАК", callback_data='tak')

    markup.add(item4)

    bot.send_message(message.chat.id, 'Ти впевнений?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:            
            if call.data == 'tak':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("📲✍🏻 Зв'язок з менеджером", url='https://t.me/YuraBossAutoUkraine')
                item2 = types.InlineKeyboardButton("🔎🚗 Індивідуальний підбір авто", url = 'https://forms.gle/ynPfcTESRjfDdaiYA')
                item3 = types.InlineKeyboardButton("📞📟 Контакти на сайті", url = "https://bossautoukraine.com.ua/")

                markup.add(item1, item2, item3)
                bot.send_message(config.owner, text_post, reply_markup=markup,
                    parse_mode="Markdown")

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пост з процедурою доставки опублікований!!",
                    reply_markup=None)     
 
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            text="Готово")

    except Exception as e:
        print(repr(e))

while True:
    try:
        bot.polling(none_stop=True)
    except OSError:
        bot.polling(none_stop=True)
