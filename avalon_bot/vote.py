import tools
import telebot
from setup import bot, bot_send_message


def add_roles_btn(game_info):
    keyboard = telebot.types.InlineKeyboardMarkup()
    symbs = {'Lady': game_info.lady_lake, 'Morgana': game_info.additional_roles['Morgana'],
             'Mordred': game_info.additional_roles['Mordred'],
             'Oberon': game_info.additional_roles['Oberon']}
    for key in symbs.keys():
        if symbs[key]:
            symbs[key] = ' ✅'
        else:
            symbs[key] = ''
    morgana_button = telebot.types.InlineKeyboardButton(text="Morgana" + symbs['Morgana'], callback_data="Morgana")
    mordred_button = telebot.types.InlineKeyboardButton(text="Mordred" + symbs['Mordred'], callback_data="Mordred")
    oberon_button = telebot.types.InlineKeyboardButton(text="Oberon" + symbs['Oberon'], callback_data="Oberon")
    lady_button = telebot.types.InlineKeyboardButton(text="Lady of the Lake" + symbs['Lady'],
                                                     callback_data="Lady of the Lake")
    keyboard.add(mordred_button, morgana_button, oberon_button, lady_button)
    return keyboard


def vote_keyboard(chat_id, game_info):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(0, len(game_info.players)):
        symb = ''
        if game_info.order[i] in game_info.cur_exp:
            symb = ' ✅'
        btn = telebot.types.InlineKeyboardButton(
            text='@' + str(bot.get_chat_member(chat_id, game_info.order[i]).user.username) + symb,
            callback_data='v ' + str(game_info.order[i]))
        keyboard.add(btn)
    return keyboard


def send_voting(chat_id, game_info):
    msg = bot_send_message(chat_id, "Choose expeditors", reply_markup=vote_keyboard(chat_id, game_info))
    game_info.vote_msg_id = msg.message_id
    keybord = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton(text="Send", callback_data="send_expedition")
    keybord.add(btn)
    del_m = bot_send_message(chat_id, "Send expedition", reply_markup=keybord)
    try:
        bot.pin_chat_message(chat_id, msg.message_id)  # Govno tut
    except:
        pass
    game_info.del_msg.append(msg.message_id)
    game_info.del_msg.append(del_m.message_id)
