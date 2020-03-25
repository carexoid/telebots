import telebot
import teletoken
from tools import GameInfo

bot = telebot.TeleBot(teletoken.token)


def vote_for_exp(expeditors, chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row('👍I like this expedition', '👎🏿I don`t like it')
    for player_id in expeditors:
        bot.send_message(player_id, 'Do you like this expedition?', reply_markup=keyboard)


def start_exp(expeditors, chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row('❤️ Approve', '🖤 Reject')
    for player_id in expeditors:
        bot.send_message(player_id, 'Your choice in expedition', reply_markup=keyboard)


def exp_successful(red_cards, num_of_expeditors, num_of_exp, num_of_players):
    if num_of_players > 6 and num_of_exp == 3 and red_cards + 1 == num_of_expeditors:
        return True, 1
    return red_cards == num_of_expeditors, num_of_expeditors - red_cards


def lady_check(chat_id, game_info):
    if not game_info.lady_lake:
        return
    keyboard = telebot.types.InlineKeyboardMarkup()
    for player in game_info.order:
        if player not in game_info.checked:
            cur_button = telebot.types.InlineKeyboardButton(
                text='\n@' + str(bot.get_chat_member(chat_id, player).user.username),
                callback_data=str(player) + ' ' + str(chat_id))
            keyboard.add(cur_button)
    bot.send_message(game_info.order[game_info.cur_lady], "Who do you want to check?", reply_markup=keyboard)


def endgame(chat_id, game_info, dead_id):
    if game_info.players[dead_id] == 'Merlin':
        bot.send_message(chat_id, 'Merlin was killed')
    else:
        bot.send_message(chat_id, 'Merlin is alive!\n' + game_info.players[dead_id] + ' was killed')
    string = ''
    for item in game_info.players.items():
        string += '\n' + bot.get_chat_member(chat_id, item[0]).user.username + ' was ' + \
                  ('❤️' if item[1] in tools.GameInfo.peaceful else '🖤') + item[1]
    bot.send_message(chat_id, 'Roles in this game:' + string)

