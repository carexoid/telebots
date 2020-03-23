import telebot
import teletoken
from tools import GameInfo

bot = telebot.TeleBot(teletoken.token)


def vote_for_exp(expeditors, chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('I like this expedition in chat ' + str(chat_id), 'I don`t like it in chat ' + str(chat_id))
    for player_id in expeditors:
        bot.send_message(player_id, 'Do you like this expedition?', reply_markup=keyboard)


def start_exp(expeditors, chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('Peace in chat ' + str(chat_id), 'War in chat ' + str(chat_id))
    for player_id in expeditors:
        bot.send_message(player_id, 'Your choice in expedition', reply_markup=keyboard)


def exp_successful (red_cards, num_of_expeditors, num_of_exp):
    return red_cards == num_of_expeditors


def lady_check(chat_id, game_info):
    if not game_info.lady_lake:
        return
    keyboard = telebot.types.InlineKeyBoardMarkup();
    for player in game_info.order:
        cur_button = telebot.types.InlineKeyboardButton(text='\n@' + str(bot.get_chat_member(chat_id, player).user.username), callback_data=str(player) + str(chat_id))
        keyboard.add(cur_button)
    bot.send_message(game_info.order[cur_lady], "Who do you want to check?", reply_markup=keyboard)