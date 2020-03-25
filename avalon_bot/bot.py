import telebot
import teletoken
import tools
import gameplay
import roles
import random

bot = telebot.TeleBot(teletoken.token)

players_id = dict()


@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, 'yooooy')

@bot.message_handler(commands=['leave'])
def start(msg):
    for chat in players_id:
        if msg.from_user.id in players_id[chat].players:
            del players_id[chat].players[msg.from_user.id]

        keyboard = telebot.types.InlineKeyboardMarkup()
        add_button = telebot.types.InlineKeyboardButton(text="Register", callback_data="register")
        keyboard.add(add_button)
        reg_msg = players_id[chat].reg_btn
        reg = 'Registration is on\nPlayers in game:'
        for user in players_id[chat].players:
            reg = reg + ' @' + str(bot.get_chat_member(chat, user).user.username)

        print(reg)
        bot.edit_message_text(chat_id=chat, message_id=reg_msg.message_id, text=reg,
                              reply_markup=keyboard)
        bot.send_message(msg.from_user.id, "You have left the game")


@bot.message_handler(commands=['start_registration'])
def start_reg(msg):
    try:
        players_id[msg.chat.id]
    except KeyError:
        players_id[msg.chat.id] = tools.GameInfo('reg', msg.from_user.id, dict(), msg)
        keyboard = telebot.types.InlineKeyboardMarkup()
        add_button = telebot.types.InlineKeyboardButton(text="Register", callback_data="register")
        keyboard.add(add_button)
        bot.reply_to(msg, 'Registration is on\nPlayers in game:', reply_markup=keyboard)
        bot.send_message(msg.from_user.id, 'You`re creator of game in chat ' + str(msg.chat.id) + '\n Only you can '
                                                                                                  'launch the game')
        return
    bot.reply_to(msg, ('Game' if players_id[msg.chat.id].state == 'game' else 'Registration') + ' is on!')


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
            print(players_id[msg.chat.id].players)
            # players_id[msg.chat.id].players = role.make_roles(players_id[msg.chat.id].players)
            players_id[msg.chat.id].cur_voting_for_exp = dict.copy(players_id[msg.chat.id].players)
            bot.send_message(msg.from_user.id, " You have launched the game in" + str(msg.chat.id))
            roles.make_roles(players_id[msg.chat.id].players, players_id[msg.chat.id].additional_roles)
            players_id[msg.chat.id].order = list(players_id[msg.chat.id].players.keys())
            random.shuffle(players_id[msg.chat.id].order)
            string = ''
            for i in range(0, len(players_id[msg.chat.id].order)):
                string += '\n' + str(i + 1) + '. @' \
                          + str(bot.get_chat_member(msg.chat.id, players_id[msg.chat.id].order[i]).user.username)
            bot.send_message(msg.chat.id, 'Players order:' + string)
            players_id[msg.chat.id].cur_king = 0
            players_id[msg.chat.id].cur_lady = -1
            players_id[msg.chat.id].checked.append(players_id[msg.chat.id].order[-1])
            king_id = players_id[msg.chat.id].order[players_id[msg.chat.id].cur_king]
            bot.send_message(msg.chat.id, "King is @" + str(bot.get_chat_member(msg.chat.id, king_id).user.username))
            if players_id[msg.chat.id].lady_lake:
                lady_id = players_id[msg.chat.id].order[players_id[msg.chat.id].cur_lady]
                bot.send_message(msg.chat.id,
                                 "Lady of the Lake is @" + str(bot.get_chat_member(msg.chat.id, lady_id).user.username))
            print(players_id[msg.chat.id].players)
            print(players_id[msg.chat.id].order)
            print(players_id[msg.chat.id].players_nick_to_id)
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
            lady_button = telebot.types.InlineKeyboardButton(text="Lady of the Lake", callback_data="Lady of the Lake")
            keyboard.add(mordred_button, morgana_button, oberon_button, lady_button)
            bot.send_message(msg.chat.id, "What role do you want to add?", reply_markup=keyboard)
    except KeyError:
        bot.reply_to(msg, 'No registration started\nRun /start_registration')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    if call.message:
        if call.data[0] == 'a' and call.data[1] == '@':
            nickname = call.data[1:len(call.data)]
            players_nick_to_id = players_id[chat_id].players_nick_to_id
            role = players_id[chat_id].players[players_nick_to_id[nickname]]
            bot.send_message(chat_id, nickname + " was " + role)
            if role == 'Merlin':
                bot.send_message(chat_id, "Mordred wins")
            else:
                bot.send_message(chat_id, 'Avalon wins')

        elif call.data == "register":
            try:
                players_id[int(call.message.chat.id)]
            except KeyError:
                bot.reply_to(call.message, 'No registration started!\nRun /start_registration')
                return
            if players_id[call.message.chat.id].state == 'reg':
                if int(call.from_user.id) not in players_id[int(call.message.chat.id)].players:
                    players_id[int(call.message.chat.id)].players[int(call.from_user.id)] = None
                    players_id[int(call.message.chat.id)].players_nick_to_id['@' + call.from_user.username] = \
                        int(call.from_user.id)
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    add_button = telebot.types.InlineKeyboardButton(text="Register", callback_data="register")
                    keyboard.add(add_button)
                    text = call.message.text + ' @' + call.from_user.username
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                                          reply_markup=keyboard)
                    players_id[call.message.chat.id].reg_btn = call.message
                    bot.send_message(call.from_user.id,
                                     'You`re registered for the Avalon game in ' + call.message.chat.title)

                #bot.send_message(chat_id, len(players_id[int(chat_id)]))
            else:
                bot.reply_to(call.message, 'Game is on!')


        elif call.data == "Lady of the Lake":
            out = players_id[chat_id].change_lady()
            bot.send_message(chat_id, call.data + out)
        elif call.data == "Morgana" or call.data == "Oberon" or call.data == "Mordred":
            out = players_id[chat_id].change_roles(call.data)
            bot.send_message(chat_id, call.data + out)

        else:
            data = call.data.split()
            nickname = str(bot.get_chat_member(data[1], data[0]).user.username)
            chat = int(data[1])
            user = int(data[0])
            lady_id = players_id[chat].order[players_id[chat].cur_lady]
            bot.send_message(chat, "Lady of the Lake has checked @" + nickname)
            #bot.send_message(chat, '@' + nickname + ' is new Lady of the Lake')
            #index = 0
            #i = 0
            #print("order", players_id[chat].order)
            #for i in players_id[chat].order:
            #    print(i, user)
            #    if i == user:
            #        print("lady index = ", index)
            #        index = i
            #    i = i + 1
            #players_id[chat].cur_lady = index
            check = ''
            if players_id[chat].players[user] == 'Merlin' or players_id[chat].players[user] == 'Persival' or \
                    players_id[chat].players[user] == 'Loyal Servant of Arthur':
                check = " is servant of Arthur"
            else:
                check = " is servant of Mordred"
            bot.send_message(lady_id, nickname + check)


@bot.message_handler(commands=['vote_for_expedition'])
def voter(msg):
    try:
        if msg.from_user.id != players_id[msg.chat.id].order[players_id[msg.chat.id].cur_king]:
            bot.reply_to(msg, 'You aren`t the king, durik!!!')
            return
        if len(msg.text.split()) < 1:
            bot.reply_to(msg, 'To few expeditors')
        else:
            exp_id = []
            nicks = msg.text.split()
            nicks.pop(0)
            for nick in nicks:
                print(nick)
                exp_id.append(players_id[msg.chat.id].players_nick_to_id[nick])
            for player in players_id[msg.chat.id].players.keys():
                players_id[msg.chat.id].cur_voting_for_exp[player] = None
            gameplay.vote_for_exp(players_id[msg.chat.id].order, msg.chat.id)
            players_id[msg.chat.id].cur_exp = exp_id
            players_id[msg.chat.id].state = 'vote'
    except KeyError:
        bot.reply_to(msg, 'No registration started\nRun /start_registration')


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
        chat_id = int(msg.text.split().pop())
        if players_id[chat_id].state == 'vote':
            print(msg.text)
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
                                + (' 👍' if players_id[chat_id].cur_voting_for_exp[player] == 1 else ' -1')
            bot.send_message(chat_id,
                             (
                                 'there will be such expedition' if sum > 0 else 'There won`t be such expedition') + people_votes)
            if sum > 0:
                players_id[chat_id].state = 'exp'
                players_id[chat_id].people_in_exp = dict()
                for id in players_id[chat_id].cur_exp:
                    players_id[chat_id].people_in_exp[id] = None
                gameplay.start_exp(players_id[chat_id].cur_exp, chat_id)
            else:
                players_id[chat_id].state = 'game'
                players_id[chat_id].king_rotation()
                string = ''
                for i in range(0, len(players_id[chat_id].order)):
                    string += '\n' + str(i + 1) + '. @' \
                              + str(bot.get_chat_member(chat_id, players_id[chat_id].order[i]).user.username)
                bot.send_message(chat_id, 'Players order:' + string)
                bot.send_message(chat_id, 'New King is @' + str(bot.get_chat_member(chat_id, players_id[chat_id].order[players_id[chat_id].cur_king]).user.username))
        else:
            bot.reply_to(msg, 'No voting for expedition right now!')

    except KeyError:
        print('bot durila')


@bot.message_handler(func=lambda message: message.text and ("Peace in chat " in message.text
                                                            or 'War in chat ' in message.text))
def get_exp_choice(msg):
    try:
        chat_id = int(msg.text.split().pop())
        if (players_id[chat_id].state != 'exp'):
            return
        if players_id[chat_id].people_in_exp[msg.from_user.id] is None:
            players_id[chat_id].people_in_exp[msg.from_user.id] = 1 if msg.text.split()[0] == 'Peace' else 0
        sum = 0
        for choice in players_id[chat_id].people_in_exp.values():
            if choice is None:
                return
            sum += choice
        print(sum)
        num_of_exp = players_id[chat_id].successful_exp + players_id[chat_id].failed_exp
        exp_res = gameplay.exp_successful(sum, len(players_id[chat_id].people_in_exp), num_of_exp, len(players_id[chat_id].order))
        print(exp_res)
        if exp_res[0]:
            bot.send_message(chat_id, 'Expedition was successful\nNum of black cards is ' + str(exp_res[1]))
            players_id[chat_id].successful_exp += 1
        else:
            bot.send_message(chat_id, 'Expedition was failed\nNum of black cards is ' + str(exp_res[1]))
            players_id[chat_id].failed_exp += 1
        if players_id[chat_id].failed_exp == 3:
            bot.send_message(chat_id, 'RIP Avalon!')
        elif players_id[chat_id].successful_exp == 3:
            keyboard = telebot.types.InlineKeyboardMarkup()
            for id in players_id[chat_id].players:
                if players_id[chat_id].players[id] == "Loyal Servant of Arthur" or players_id[chat_id].players[id] == \
                        'Merlin' or players_id[chat_id].players[id] == 'Percival':
                    nickname = '@' + str(bot.get_chat_member(chat_id, id).user.username)
                    btn = telebot.types.InlineKeyboardButton(text=nickname, callback_data='a' + nickname)
                    keyboard.add(btn)
            bot.send_message(chat_id, 'Time to shot for Assassin')
            for i in players_id[chat_id].players:
                if players_id[chat_id].players[i] == "Assassin":
                    bot.send_message(i, "Who do you want to kill?", reply_markup=keyboard)

        else:
            players_id[chat_id].state = 'game'
            players_id[chat_id].king_rotation()
            string = ''
            for i in range(0, len(players_id[chat_id].order)):
                string += '\n' + str(i + 1) + '. @' \
                          + str(bot.get_chat_member(chat_id, players_id[chat_id].order[i]).user.username)
            bot.send_message(chat_id, 'Players order:' + string)
            bot.send_message(chat_id, 'New King is @' + str(bot.get_chat_member(chat_id, players_id[chat_id].order[players_id[chat_id].cur_king]).user.username))
            if (players_id[chat_id].get_num_of_exp() > 1):
                gameplay.lady_check(chat_id, players_id[chat_id])

    except KeyError:
        print('bot durila x2')


if __name__ == '__main__':
    bot.polling()
