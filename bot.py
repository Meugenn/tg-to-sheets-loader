import telebot
import const
from funcs import *
import re
import spreadsheet
from flask import Flask, request
import os

bot = telebot.TeleBot(const.bot_token)
server = Flask(__name__)
errors_text = ''

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
    try:
        if re.match(list_for_regexp.lower(), message.text.lower()):
            subject = re.match(list_for_regexp.lower(), message.text.lower()).group()
            subject = list_of_subjects_in_low[subject]
            text_homework = message.text[len(subject)+1:]
            if text_homework[0] == ' ':
                text_homework = text_homework[1:]
            spreadsheet.update_homework(subject, text_homework)
            bot.reply_to(message, 'Отлично, твое дз сохранено!')
    except Exception as e:
        global errors_text
        errors_text += str(e) + '\n'

@server.route('/' + const.bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://dzxa-loader.herokuapp.com/' + const.bot_token)
    return '\n'.join(list_of_subjects) + '\n' + errors_text, 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))