import telebot
import sqlite3
import random
from teletoken import token

conn = sqlite3.connect('sTaS.db')
bot = telebot.TeleBot(token)

users_id = dict()


@bot.message_handler(commands=['start'])
def start_message(msg):
    if msg.chat.id not in users_id.keys():
        users_id[msg.chat.id] = dict()
        users_id[msg.chat.id]['all'] = []
    bot.send_sticker(msg.chat.id, "CAACAgIAAxkBAAMNXmY0Gb3evIOJEvQH26a40StBDQwAAhYBAALzVj8XeDGXQtN-xgcYBA")


@bot.message_handler(content_types=['sticker'])
def receive_sticker(stckr):
    print(stckr)


@bot.message_handler(commands=['hi_rightless'])
def Say_hello(msg):
    if msg.chat.id not in users_id.keys():
        users_id[msg.chat.id] = dict()
        users_id[msg.chat.id]['all'] = []
    cur_users_id = users_id[msg.chat.id]['all']
    if msg.from_user.id not in cur_users_id:
        cur_users_id.append(msg.from_user.id)
    print(users_id)
    bot.send_sticker(msg.chat.id, "CAACAgIAAxkBAAMvXmY70ZzdsmncwzrQmiAelSD3Z5EAAm8BAALzVj8XnZO2J6flZasYBA",
                     reply_to_message_id=msg.message_id)


@bot.message_handler(commands=['tag_all'])
def tag_message(msg):
    if msg.chat.id not in users_id.keys():
        users_id[msg.chat.id] = dict()
        users_id[msg.chat.id]['all'] = []
    cur_users_id = users_id[msg.chat.id]['all']
    tags = ''
    for user_id in cur_users_id:
        user = bot.get_chat_member(msg.chat.id, user_id).user
        tags += '@' + user.username + ' '
    if tags:
        bot.send_message(msg.chat.id, tags)
    else:
        bot.send_message(msg.chat.id, 'Ну и кого ты тегать собрался, дурик. Я шо ебу как вас зовут?')


@bot.message_handler(commands=['create_group'])
def create_group(msg):
    if msg.chat.id not in users_id.keys():
        users_id[msg.chat.id] = dict()
        users_id[msg.chat.id]['all'] = []
    try:
        group_name = msg.text.split()[1]
        print(group_name)
        users_id[msg.chat.id][group_name] = []
        bot.send_message(msg.chat.id, 'Ты создал групировку: ' + group_name, reply_to_message_id=msg.message_id)
    except IndexError:
        bot.send_message(msg.chat.id, 'А название ты не хочешь указать?', reply_to_message_id=msg.message_id)


@bot.message_handler(commands=['join_group'])
def join_group(msg):
    if msg.chat.id not in users_id.keys():
        users_id[msg.chat.id] = dict()
        users_id[msg.chat.id]['all'] = [msg.from_user]
    try:
        group_name = msg.text.split()[1]
        if group_name not in users_id[msg.chat.id].keys():
            users_id[msg.chat.id][group_name] = []
        users_id[msg.chat.id][group_name].append(msg.from_user.id)
        bot.send_message(msg.chat.id, 'Ты теперь в групировке: ' + group_name, reply_to_message_id=msg.message_id)
    except IndexError:
        bot.send_message(msg.chat.id, 'А название ты не хочешь указать?', reply_to_message_id=msg.message_id)


@bot.message_handler(commands=['tag_group'])
def tag_group(msg):
    if msg.chat.id not in users_id.keys():
        users_id[msg.chat.id] = dict()
        users_id[msg.chat.id]['all'] = []
    try:
        group_name = msg.text.split()[1]
    except IndexError:
        bot.send_message(msg.chat.id, 'А название ты не хочешь указать?', reply_to_message_id=msg.message_id)
        return

    try:
        cur_users_id = users_id[msg.chat.id][group_name]
    except KeyError:
        bot.send_message(msg.chat.id, 'Нет такой групировки', reply_to_message_id=msg.message_id)
        return

    tags = ''
    for user_id in cur_users_id:
        user = bot.get_chat_member(msg.chat.id, user_id).user
        tags += '@' + user.username + ' '
    if tags:
        bot.send_message(msg.chat.id, tags)
    else:
        bot.send_message(msg.chat.id, 'Ну и кого ты тегать собрался, дурик. Я шо ебу как вас зовут?')

@bot.message_handler(commands=['try'])
def try_text(msg):
    bot.send_message(msg.chat.id, 'И правда)', reply_to_message_id=msg.message_id) if random.randint(0, 1) else bot.send_message(msg.chat.id, 'Пиздеж!!', reply_to_message_id=msg.message_id)


bot.polling()

