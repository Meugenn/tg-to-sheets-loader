import telebot
import const
from funcs import *
import re
import spreadsheet
from flask import Flask, request

bot = telebot.TeleBot(const.bot_token)
server = Flask(__name__)

list_of_subjects = get_subjects()
list_of_subjects_in_low = {}
for sub in list_of_subjects:
    list_of_subjects_in_low[sub.lower()] = sub
list_for_regexp = "(" + ")|(".join(list_of_subjects) + ")"
@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = '''<b>Привет, я заливаю дз в google sheets</b>
    
Чтобы я воспринял его, когда скидываешь дз пиши Название_предмета- дз. (Вместо тире можно двоеточие). Все что будет после тире будет залито в таблицу

Названия предметов: '''
    text += ', '.join(list_of_subjects)
    bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def subject_updater(message):
    if re.match(list_for_regexp.lower(), message.text.lower()):
        subject = re.match(list_for_regexp.lower(), message.text.lower()).group()
        subject = list_of_subjects_in_low[subject]
        text_homework = message.text[len(subject)+1:]
        if text_homework[0] == ' ':
            text_homework = text_homework[1:]
        spreadsheet.update_homework(subject, text_homework)
        bot.reply_to(message, 'Отлично, твое дз сохранено!')


bot.polling(none_stop=True)
