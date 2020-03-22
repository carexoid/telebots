import telebot
import teletoken
import tools
import gameplay
import roles

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
        bot.send_message(msg.from_user.id, 'You`re creator of game in chat ' + str(msg.chat.id) + '\n Only you can '
                                                                                                  'launch the game')
        return
    bot.reply_to(msg, ('Game' if players_id[msg.chat.id].state == 'game' else 'Registration') + ' is on!')


@bot.message_handler(commands=['reg_me'])
def reg_user(msg):
    try:
        players_id[msg.chat.id]
    except KeyError:
        bot.reply_to(msg, 'No registration started!\nRun /start_registration')
        return
    if players_id[msg.chat.id].state == 'reg':
        if msg.from_user.id not in players_id[msg.chat.id].players:
            players_id[msg.chat.id].players[msg.from_user.id] = None
            players_id[msg.chat.id].players_nick_to_id['@' + msg.from_user.username] = msg.from_user.id
        bot.reply_to(msg, 'You`re registered!')
    else:
        bot.reply_to(msg, 'Game is on!')


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
            players_id[msg.chat.id].cur_voting_for_exp = dict.copy(players_id[msg.chat.id].players)
            bot.send_message(msg.from_user.id, " You have launched the game in" + str(msg.chat.id))
            roles.make_roles(players_id[msg.chat.id].players, tools.GameInfo.additional_roles)
        else:
            bot.reply_to(msg, 'You`re not creator of this game!')
        players_id[msg.chat.id].state = 'game'
    print(players_id[msg.chat.id].players)


@bot.message_handler(commands=['add_roles'])
def add_roles(msg):
    try:

        if players_id[msg.chat.id].state == 'game':
            bot.reply_to(msg, "The game has already started")
        else:
            keyboard = telebot.types.InlineKeyboardMarkup()
            morgana_button = telebot.types.InlineKeyboardButton(text="Morgana", callback_data="Morgana")
            mordred_button = telebot.types.InlineKeyboardButton(text="Mordred", callback_data="Mordred")
            oberon_button = telebot.types.InlineKeyboardButton(text="Oberon", callback_data="Oberon")
            lady_button = telebot.types.InlineKeyboardButton(text="Lady of the Lake", callback_data="Lady")
            keyboard.add(mordred_button, morgana_button, oberon_button, lady_button)
            bot.send_message(msg.chat.id, "What role do you want to add?", reply_markup=keyboard)
    except KeyError:
        bot.reply_to(msg, 'No registration started\nRun /start_registration')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "Lady":
            if tools.GameInfo.lady_lake:
                bot.send_message(call.message.chat.id, "Lady of the Lake has removed")
                tools.GameInfo.lady_lake = False
            else:
                bot.send_message(call.message.chat.id, "Lady of the Lake has added")
                tools.GameInfo.lady_lake = True
        else:
            if tools.GameInfo.additional_roles[call.data]:
                bot.send_message(call.message.chat.id, call.data + " has removed")
                tools.GameInfo.additional_roles[call.data] = False
            else:
                bot.send_message(call.message.chat.id, call.data + " has added")
                tools.GameInfo.additional_roles[call.data] = True


@bot.message_handler(commands=['vote_for_expedition'])
def voter(msg):
    if len(msg.text.split()) < 4:
        bot.reply_to(msg, 'To few expeditors')
    else:
        exp_id = []
        nicks = msg.text.split()
        nicks.pop(0)
        for nick in nicks:
            print(nick)
            exp_id.append(players_id[msg.chat.id].players_nick_to_id[nick])
        gameplay.vote_for_exp(exp_id, msg.chat.id)
        players_id[msg.chat.id].cur_exp = exp_id
        players_id[msg.chat.id].state = 'vote'


@bot.message_handler(commands=['abort'])
def abort(msg):
    try:
        if msg.from_user.id == players_id[msg.chat.id].creator:
            players_id.pop(msg.chat.id)
            bot.reply_to(msg, 'Game aborted')
        else:
            bot.reply_to(msg, 'You`re not creator of this game!')
    except KeyError:
        bot.reply_to(msg, 'No game to be aborted')


@bot.message_handler(func=lambda message: message.text and ("I like this expedition in chat " in message.text
                                          or 'I don`t like it in chat ' in message.text))
def get_vote(msg):
    try:
        print(msg.text)
        chat_id = int(msg.text.split().pop())
        print(chat_id)
        if not players_id[chat_id].cur_voting_for_exp[msg.from_user.id]:
            players_id[chat_id].cur_voting_for_exp[msg.from_user.id] = (1 if msg.text.split()[1] == 'like' else -1)
            keyboard = telebot.types.ReplyKeyboardMarkup()
            bot.send_message(msg.chat.id, "You voted for this expedition", reply_markup=None)
        sum = 0
        people_votes = ''
        for vote in players_id[chat_id].cur_voting_for_exp.values():
            if not vote:
                return
            sum += int(vote)
        for player in players_id[chat_id].cur_voting_for_exp.keys():
            people_votes += '\n@' + str(bot.get_chat_member(chat_id, player).user.username) \
                            + (' +1' if players_id[chat_id].cur_voting_for_exp[player] == 1 else ' -1')
        bot.send_message(chat_id,
                         ('there will be such expedition' if sum > 0 else 'There won`t be such expedition') + people_votes)
        if sum > 0:
            players_id[chat_id].state = 'exp'
            gameplay.start_exp(players_id[chat_id].cur_exp, chat_id)
        else:
            players_id[chat_id].state = 'game'
    except KeyError:
        print('bot durila')

bot.polling()
