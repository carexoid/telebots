import tools
import telebot
import teletoken

bot = telebot.TeleBot(teletoken.token)


def vote_keyboard(chat_id, game_info):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(0, len(game_info.players)):
        symb = ''
        print(game_info.order[i], "and", game_info.cur_exp)
        if game_info.order[i] in game_info.cur_exp:
            print("added")
            symb = ' ✅'
        btn = telebot.types.InlineKeyboardButton(
            text='@'+str(bot.get_chat_member(chat_id, game_info.order[i]).user.username)+symb,
            callback_data='v ' + str(game_info.order[i]))
        keyboard.add(btn)
    return keyboard


def send_voting(chat_id, game_info):
    msg = bot.send_message(chat_id, "Choose expeditors", reply_markup=vote_keyboard(chat_id, game_info))
    bot.pin_chat_message(chat_id, msg.message_id)
    game_info.vote_msg_id = msg.message_id

