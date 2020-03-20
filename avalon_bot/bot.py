import telebot
import teletoken
import tools

bot = telebot.TeleBot(teletoken.token)

players_id = dict()

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, 'yooooy')

@bot.message_handler(commands=['start_registration'])
def start_reg(msg):
    try:
        players_id[msg.chat.id]
    except KeyError:
        players_id[msg.chat.id] = tools.GameInfo('reg', msg.from_user.id, dict())
        bot.reply_to(msg, 'Registration is on')
        bot.send_message(msg.from_user.id, 'You`re creator of game in chat ' + str(msg.chat.id) + '\n Only you can launch the game')
        return
    bot.reply_to(msg, ('Game' if players_id[msg.chat.id].state == 'game' else 'Registration') + ' is on!')

@bot.message_handler(commands=['reg_me'])
def reg_user(msg):
    try:
        players_id[msg.chat.id]
    except KeyError:
        bot.reply_to(msg, 'No registration started!\nRun /start_registration')
        return
    if msg.from_user.id not in players_id[msg.chat.id].players:
        players_id[msg.chat.id].players[msg.from_user.id] = None
    bot.reply_to(msg, 'You`re registered!')

@bot.message_handler(commands=['end_registration'])
def end_reg(msg):
    try:
        players_id[msg.chat.id]
    except KeyError:
        bot.reply_to(msg, 'No registration started!\nRun /start_registration')
        return
    if players_id[msg.chat.id].state == 'game':
        bot.reply_to(msg, 'Game is on!')
    else:
        if msg.from_user.id == players_id[msg.chat.id].creator:
            # players_id[msg.chat.id].players = role.make_roles(players_id[msg.chat.id].players)
            bot.send_message(msg.from_user.id, " You have launched the game in" + str(msg.chat.id))
        else:
            bot.reply_to(msg, 'You`re not creator of this game!')
        players_id[msg.chat.id].state = 'game'
    print(players_id[msg.chat.id].players)



bot.polling()