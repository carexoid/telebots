import telebot
import teletoken

bot = telebot.TeleBot(teletoken.token)

def vote_for_exp(expeditors, chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('I like this expedition in chat ' + str(chat_id), 'I don`t like it in chat ' + str(chat_id))
    for player_id in expeditors:
        bot.send_message(player_id, 'Do you like this expedition?', reply_markup=keyboard)
