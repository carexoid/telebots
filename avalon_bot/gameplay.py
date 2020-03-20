import telebot
import teletoken

bot = telebot.TeleBot(teletoken.token)

def vote_for_exp(expeditors, chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('I like this expedition in chat ' + str(chat_id), 'i don`t like it in chat ' + str(chat_id))
    bot.send_message
