import telebot
import tools
import gameplay
import roles
import random
import vote
from language import State, Language

from global_variables import players_id, chat_of_player, languages
from setup import bot, bot_send_message


@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_sticker(msg.chat.id, "CAACAgIAAxkBAAMvXmY70ZzdsmncwzrQmiAelSD3Z5EAAm8BAALzVj8XnZO2J6flZasYBA",
                     reply_to_message_id=msg.message_id)


@bot.message_handler(commands=['leave'])
def leave(msg):
    if msg.from_user.id not in chat_of_player:
        try:
            bot_send_message(msg.from_user.id, languages[msg.chat.id]["You don`t take part in any game"])
        except KeyError:
            bot_send_message(msg.from_user.id, "You don`t take part in any game")

        return
    if players_id[chat_of_player[msg.from_user.id]].state != 'reg':
        if msg.from_user.id not in chat_of_player.keys():
            return
        bot.reply_to(msg, languages[msg.chat.id]['You have left the game'])
        currChat = chat_of_player[msg.from_user.id]
        if players_id[currChat].players[msg.from_user.id] == "Merlin":
            bot_send_message(currChat, languages[msg.chat.id]['Merlin has left the game'] + '\n\n' + languages[msg.chat.id]['RIP Avalon!!'])
            for id in players_id[currChat].del_msg:
                bot.delete_message(chat_id=currChat, message_id=id)
            string = ""
            for item in players_id[currChat].players.items():
                string += '\n@' + bot.get_chat_member(currChat, item[0]).user.username + languages[msg.chat.id][' was '] + \
                          ('❤️' if item[1] in tools.GameInfo.peaceful else '🖤') + item[1]
            bot_send_message(currChat, 'Roles in this game:' + string)
            for id in players_id[currChat].players:
                chat_of_player.pop(id)
            players_id.pop(currChat)
            return
        if players_id[currChat].players[msg.from_user.id] == "Assassin":
            for item in players_id[currChat].players.keys():
                if players_id[currChat].players[item] not in players_id[currChat].peaceful:
                    bot.send_message(item, languages[msg.chat.id]["You are the new Assassin"])
                    players_id[currChat].players[item] = 'Assassin'
                    break
        print(msg.from_user)
        #print(chat_of_player[currChat].order)
        #print(chat_of_player[currChat].cur_king)
        #print(msg.from_user.username)
        if players_id[currChat].order[players_id[currChat].cur_king] == msg.from_user.username:
            players_id[currChat].cur_king = (players_id[currChat].cur_king + 1) % \
                                               (len(players_id[currChat].order) - 1)
        if players_id[currChat].lady_lake and players_id[currChat].order[players_id[currChat].cur_lady] == msg.from_user.username:
            players_id[currChat].cur_lady = (players_id[currChat].cur_lady + 1) % \
                                               (len(players_id[currChat].order) - 1)
        if msg.from_user.id in players_id.keys():
            players_id.pop(msg.from_user.id)
        print(players_id[currChat].order)
        for i in range(len(players_id[currChat].order)):
            if players_id[currChat].order[i] == msg.from_user.id:
                players_id[currChat].order.pop(i)
                break
        #players_id[currChat].order.pop(msg.from_user.id)
        chat_of_player.pop(msg.from_user.id)
        players_id[currChat].players.pop(msg.from_user.id)
        if len(players_id[currChat].players) == 0:
            bot.send_message(currChat, languages[msg.chat.id]["All players have left the game"])
            for id in players_id[currChat].del_msg:
                bot.delete_message(chat_id=currChat, message_id=id)
            players_id[currChat].del_msg = []
            for player in players_id[currChat].players.keys():
                chat_of_player.pop(player)
            players_id.pop(currChat)
            bot.send_message(currChat, languages[msg.chat.id]['Game aborted'])
        return
    if msg.from_user.id in chat_of_player.keys():
        chat_of_player.pop(msg.from_user.id)
    for chat in players_id:
        if msg.from_user.id in players_id[chat].players:
            del players_id[chat].players[msg.from_user.id]

        keyboard = telebot.types.InlineKeyboardMarkup()
        add_button = telebot.types.InlineKeyboardButton(text=languages[msg.chat.id]["Register"], callback_data="register")
        keyboard.add(add_button)
        reg_msg = players_id[chat].reg_btn
        reg = languages[msg.chat.id]['Registration is on'] + '\n' + languages[msg.chat.id]['Players in game:']
        for user in players_id[chat].players:
            reg = reg + ' @' + str(bot.get_chat_member(chat, user).user.username)

        print(reg)
        try:

            bot.edit_message_text(chat_id=chat, message_id=reg_msg.message_id, text=reg,
                                  reply_markup=keyboard)
        except:
            return
        bot_send_message(msg.from_user.id, languages[msg.chat.id]["You have left the game"])


@bot.message_handler(commands=['start_registration'])
def start_reg(msg):
    try:
        players_id[msg.chat.id]
    except KeyError:
        players_id[msg.chat.id] = tools.GameInfo('reg', msg.from_user.id, dict(), msg)

        try:
            bot.send_message(msg.from_user.id, languages[msg.chat.id]['You`re creator of game in chat ']
                             + str(msg.chat.id) + '\n' + languages[msg.chat.id]['Only you can launch the game'])
        except telebot.apihelper.ApiException:
            bot_send_message(msg.chat.id, languages[msg.chat.id]['To be able to register in game, '
                                          'say /start to @Avalon117bot in private messages '
                                          'and push registration button again'])
            return
        try:
            keyboard = telebot.types.InlineKeyboardMarkup()
            add_button = telebot.types.InlineKeyboardButton(text=languages[msg.chat.id]["Register"], callback_data="register")
            keyboard.add(add_button)
            del_m = bot.reply_to(msg, languages[msg.chat.id]['Registration is on'] + '\n' + languages[msg.chat.id]['Players in game:'], reply_markup=keyboard)
            players_id[msg.chat.id].del_msg.append(del_m.message_id)
            return
        except:
            print("govna")
            return
    bot.reply_to(msg, (languages[msg.chat.id]['Game'] if players_id[msg.chat.id].state == 'game' else languages[msg.chat.id]['Registration']) + languages[msg.chat.id][' is on!'])


@bot.message_handler(commands=['end_registration'])
def end_reg(msg):
    try:
        players_id[msg.chat.id]
    except KeyError:
        try:
            bot.reply_to(msg, languages[msg.chat.id]['No registration started!'] + '\n' + languages[msg.chat.id]['Run /start_registration'])
            return
        except KeyError:
            bot.reply_to(msg, 'No registration started!' + '\n' + 'Run /start_registration')
            return
    try:
        if players_id[msg.chat.id].state == 'game':
            bot.reply_to(msg, languages[msg.chat.id]['Game is on!'])
        else:
            if msg.from_user.id == players_id[msg.chat.id].creator:
                players_id[msg.chat.id].exp_size = list.copy(
                    tools.GameInfo.expedition_size[len(players_id[msg.chat.id].players)])
                for id in players_id[msg.chat.id].del_msg:
                    bot.delete_message(chat_id=msg.chat.id, message_id=id)
                players_id[msg.chat.id].del_msg = []
                # players_id[msg.chat.id].players = role.make_roles(players_id[msg.chat.id].players)
                players_id[msg.chat.id].cur_voting_for_exp = dict.copy(players_id[msg.chat.id].players)
                bot_send_message(msg.from_user.id, languages[msg.chat.id]["You have launched the game in"] + str(msg.chat.id))
                roles.make_roles(players_id[msg.chat.id].players, players_id[msg.chat.id].additional_roles, msg.chat.id)
                players_id[msg.chat.id].order = list(players_id[msg.chat.id].players.keys())
                random.shuffle(players_id[msg.chat.id].order)

                string = ''
                players_id[msg.chat.id].cur_king = 0
                players_id[msg.chat.id].cur_lady = -1
                for i in range(0, len(players_id[msg.chat.id].order)):
                    string += '\n' + str(i + 1) + '. @' \
                              + str(bot.get_chat_member(msg.chat.id, players_id[msg.chat.id].order[i]).user.username)
                    if i == players_id[msg.chat.id].cur_king % len(players_id[msg.chat.id].order):
                        string += '👑'
                    if players_id[msg.chat.id].lady_lake and i == players_id[msg.chat.id].cur_lady % len(
                            players_id[msg.chat.id].order):
                        string += '👸'
                bot_send_message(msg.chat.id, languages[msg.chat.id]['Players order:'] + string)
                players_id[msg.chat.id].checked.append(players_id[msg.chat.id].order[-1])
                king_id = players_id[msg.chat.id].order[players_id[msg.chat.id].cur_king]
                bot_send_message(msg.chat.id,
                                 languages[msg.chat.id]["King is"] + " @" + str(bot.get_chat_member(msg.chat.id, king_id).user.username))
                chat_id = msg.chat.id
                bot_send_message(chat_id, languages[msg.chat.id]['This expedition is for '] +
                                 str(players_id[chat_id].exp_size[players_id[chat_id].get_num_of_exp()]) + languages[msg.chat.id][' people'])
                if players_id[msg.chat.id].lady_lake:
                    lady_id = players_id[msg.chat.id].order[players_id[msg.chat.id].cur_lady]
                    bot_send_message(msg.chat.id, languages[msg.chat.id]["Lady of the Lake is"] + " @" + str(
                        bot.get_chat_member(msg.chat.id, lady_id).user.username))
                    players_id[msg.chat.id].past_lady.append(lady_id)
                vote.send_voting(msg.chat.id, players_id[msg.chat.id])
                players_id[msg.chat.id].state = 'game'
            else:
                bot.reply_to(msg, languages[msg.chat.id]['You`re not creator of this game!'])

        print(players_id[msg.chat.id].players)
    except KeyError:
        bot.reply_to(msg, languages[msg.chat.id]['Wrong number of players to start, this game is for 5 - 10 players'])
    except:
        print("govniashki")


@bot.message_handler(commands=['add_roles'])
def add_roles(msg):
    try:

        if players_id[msg.chat.id].state == 'game':
            bot.reply_to(msg, languages[msg.chat.id]["The game has already started"])
        else:
            if msg.from_user.id != players_id[msg.chat.id].creator:
                bot_send_message(msg.chat.id, languages[msg.chat.id]["The game has already started"])
                return
            bot.send_message(msg.chat.id, languages[msg.chat.id][
                             "Morgana, a minion of Mordred, deceives Percival. During the beginning round where "
                             "Merlin puts his "
                             "thumb in the air to reveal himself to Percival, Morgana also raises her own thumb, "
                             "confusing Percival as to which 'Merlin' to trust."] + "\n\n" +
                             languages[msg.chat.id]["Oberon despite being a servant of Mordred, is somewhat of "
                             "a hindrance. Oberon does not reveal himself to evil players, and also they do not reveal "
                             "themselves to him. Oberon still raises his thumb for Merlin to see, however."] + "\n\n" +
                             languages[msg.chat.id]["Mordred helps the evil side because Merlin does not know his identity. As Mordred, "
                             "it is imperative that you recognize your unique situation because you "
                             "will be able to watch the votes to see how everyone votes for teams to which the other "
                             "minions belong."])
            keyboard = telebot.types.InlineKeyboardMarkup()
            morgana_button = telebot.types.InlineKeyboardButton(text=languages[msg.chat.id]["Morgana"], callback_data="Morgana")
            mordred_button = telebot.types.InlineKeyboardButton(text=languages[msg.chat.id]["Mordred"], callback_data="Mordred")
            oberon_button = telebot.types.InlineKeyboardButton(text=languages[msg.chat.id]["Oberon"], callback_data="Oberon")
            lady_button = telebot.types.InlineKeyboardButton(text=languages[msg.chat.id]["Lady of the Lake"], callback_data="Lady of the Lake")
            keyboard.add(mordred_button, morgana_button, oberon_button, lady_button)
            msg = bot_send_message(msg.chat.id, languages[msg.chat.id]["What role do you want to add?"], reply_markup=keyboard)
            players_id[msg.chat.id].del_msg.append(msg.message_id)
            players_id[msg.chat.id].additional_id = msg.message_id
    except KeyError:
        try:
            bot.reply_to(msg, languages[msg.chat.id]['No registration started!'] + '\n' + languages[msg.chat.id][
                'Run /start_registration'])
            return
        except KeyError:
            bot.reply_to(msg, 'No registration started!' + '\n' + 'Run /start_registration')
            return


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = int(call.message.chat.id)
    try:
        if call.message:
            if call.data[0] == 'a' and call.data[1] == '@':
                nickname = call.data.split()[0][1:len(call.data)]
                in_chat = int(call.data.split()[1])
                # players_nick_to_id = players_id[chat_id].players_nick_to_id
                role = players_id[in_chat].players[players_id[in_chat].players_nick_to_id[nickname]]
                # bot_send_message(chat_id, nickname + languages[msg.chat.id][" was "] + role)
                gameplay.endgame(in_chat, players_id[in_chat], players_id[in_chat].players_nick_to_id[nickname])
                if role == 'Merlin':
                    bot_send_message(in_chat, languages[chat_id]["Mordred wins"])
                else:
                    bot_send_message(in_chat, languages[chat_id]['Avalon wins'])
                for key in players_id[in_chat].players.keys():
                    chat_of_player.pop(key)
                players_id.pop(in_chat)
            elif call.data == "register":
                try:
                    players_id[int(call.message.chat.id)]
                except KeyError:
                    bot.reply_to(call.message, languages[chat_id]['No registration started!'] + '\n' +languages[chat_id]['Run /start_registration'])
                    return
                if players_id[call.message.chat.id].state == 'reg':
                    if not call.from_user.username:
                        bot_send_message(call.from_user.id, languages[chat_id]["Your telegram account has no username"])
                        return
                    if int(call.from_user.id) not in players_id[int(call.message.chat.id)].players:
                        if int(call.from_user.id) in chat_of_player.keys():
                            bot_send_message(int(call.from_user.id), languages[chat_id]['You are in not ended game!'])
                            return
                        try:

                            bot.send_message(call.from_user.id,
                                             languages[chat_id]['You`re registered for the Avalon game in '] + str(call.message.chat.title))
                        except telebot.apihelper.ApiException:
                            bot_send_message(chat_id, languages[chat_id]['To be able to register in game, '
                                                      'say /start to @Avalon117bot in private messages '
                                                      'and push registration button again'])
                            return
                        chat_of_player[int(call.from_user.id)] = int(call.message.chat.id)
                        players_id[int(call.message.chat.id)].players[int(call.from_user.id)] = None
                        players_id[int(call.message.chat.id)].players_nick_to_id['@' + call.from_user.username] = \
                            int(call.from_user.id)
                        keyboard = telebot.types.InlineKeyboardMarkup()
                        add_button = telebot.types.InlineKeyboardButton(text=languages[chat_id]["Register"], callback_data="register")
                        keyboard.add(add_button)
                        text = call.message.text + ' @' + call.from_user.username
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=text,
                                              reply_markup=keyboard)
                        players_id[call.message.chat.id].reg_btn = call.message

                    # bot_send_message(call.from_user.id, 'You`re registered for the Avalon game in ' +
                    #                  call.message.chat.title)
                    # bot_send_message(chat_id, len(players_id[int(chat_id)]))
                else:
                    bot.reply_to(call.message, languages[chat_id]['Game is on!'])
            elif call.data == "Lady of the Lake":
                if players_id[chat_id].creator != int(call.from_user.id):
                    return
                out = languages[chat_id][players_id[chat_id].change_lady()]
                keyboard = vote.add_roles_btn(players_id[chat_id], chat_id)
                bot.edit_message_reply_markup(chat_id=chat_id, message_id=players_id[chat_id].additional_id,
                                              reply_markup=keyboard)
            elif call.data == "Morgana" or call.data == "Oberon" or call.data == "Mordred":
                if players_id[chat_id].creator != int(call.from_user.id):
                    return
                out = languages[chat_id][players_id[chat_id].change_roles(call.data)]
                keyboard = vote.add_roles_btn(players_id[chat_id], chat_id)
                bot.edit_message_reply_markup(chat_id=chat_id, message_id=players_id[chat_id].additional_id,
                                              reply_markup=keyboard)
            elif call.data[0] == 'v':
                if call.from_user.id != players_id[chat_id].order[players_id[chat_id].cur_king]:
                    return
                arr = call.data.split()
                data = arr[1]
                if int(data) in players_id[chat_id].cur_exp:
                    for i in range(0, len(players_id[chat_id].cur_exp)):
                        if int(data) == players_id[chat_id].cur_exp[i]:
                            players_id[chat_id].cur_exp.pop(i)
                            break
                    keyboard = vote.vote_keyboard(chat_id, players_id[chat_id])
                    bot.edit_message_reply_markup(chat_id=chat_id, message_id=players_id[chat_id].vote_msg_id,
                                                  reply_markup=keyboard)
                else:
                    players_id[chat_id].cur_exp.append(int(data))
                    keyboard = vote.vote_keyboard(chat_id, players_id[chat_id])
                    bot.edit_message_reply_markup(chat_id=chat_id, message_id=players_id[chat_id].vote_msg_id,
                                                  reply_markup=keyboard)
            elif call.data == 'send_expedition':
                if call.from_user.id != players_id[chat_id].order[players_id[chat_id].cur_king]:
                    return
                if len(players_id[chat_id].cur_exp) != players_id[chat_id].exp_size[
                    players_id[chat_id].get_num_of_exp()]:
                    bot_send_message(chat_id, languages[chat_id]['Wrong number of expeditors'])
                    return
                string = ''
                for i in players_id[chat_id].cur_exp:
                    string += '\n@' + str(bot.get_chat_member(chat_id, i).user.username)
                bot_send_message(chat_id, languages[chat_id]["The expedition is:"] + string)
                for i in players_id[chat_id].order:
                    bot_send_message(i, languages[chat_id]["The expedition is:"] + string)
                players_id[chat_id].state = 'vote'
                gameplay.vote_for_exp(players_id[chat_id].order, chat_id)
                for id in players_id[chat_id].del_msg:
                    bot.delete_message(chat_id=chat_id, message_id=id)
                players_id[chat_id].del_msg = []
            elif call.data.split()[0] == "lang":
                if int(call.from_user.id) != int(call.data.split()[2]):
                    return
                if call.data.split()[1] == "eng":
                    print("iiiii")
                    languages[chat_id].set_lang(State.eng)
                elif call.data.split()[1] == "rus":
                    languages[chat_id].set_lang(State.rus)
                else:
                    languages[chat_id].set_lang(State.ukr)
                bot.delete_message(chat_id=chat_id, message_id=int(call.message.message_id))

            else:
                data = call.data.split()
                chat = int(data[1])
                user = int(data[0])
                nickname = str(bot.get_chat_member(chat, user).user.username)
                lady_id = players_id[chat].order[players_id[chat].cur_lady]
                bot_send_message(chat, languages[chat]["Lady of the Lake has checked"] + " @" + nickname)
                players_id[chat].pass_lady(user)
                players_id[chat].past_lady.append(user)
                check = ''
                if players_id[chat].players[user] in players_id[chat].peaceful:
                    check = languages[chat][" is servant of Arthur"]
                else:
                    check = languages[chat][" is servant of Mordred"]
                bot_send_message(lady_id, '@' + nickname + check)
                bot_send_message(chat, '@' + nickname + languages[chat][" is new Lady of the Lake"])
                try:
                    players_id[chat].cur_exp = []
                    for player in players_id[chat].players.keys():
                        players_id[chat].cur_voting_for_exp[player] = None
                    vote.send_voting(chat, players_id[chat])
                except KeyError:
                    print(KeyError)

    except telebot.apihelper.ApiException:
        print("Stop DDOSing buttons!")
    except KeyError:
        try:
            bot_send_message(chat_id, languages[chat_id]["Don`t touch old buttons, run /start_registration first!"])
        except:
            bot_send_message(chat_id, "Don`t touch old buttons, run /start_registration first!")


@bot.message_handler(commands=['abort'])  # ЦЕ ГРЕХ, ДАНЯ, ПОДУМАЙ!!
def abort(msg):
    try:
        if msg.from_user.id == players_id[msg.chat.id].creator:
            for id in players_id[msg.chat.id].del_msg:
                bot.delete_message(chat_id=msg.chat.id, message_id=id)
            players_id[msg.chat.id].del_msg = []
            for player in players_id[msg.chat.id].players.keys():
                chat_of_player.pop(player)
            players_id.pop(msg.chat.id)
            bot.reply_to(msg, languages[msg.chat.id]['Game aborted'])
        else:
            bot.reply_to(msg, languages[msg.chat.id]['You`re not creator of this game!'])
    except KeyError:
        try:
            bot.reply_to(msg, languages[msg.chat.id]['No game to be aborted'])
        except KeyError:
            bot.reply_to(msg, 'No game to be aborted')


@bot.message_handler(commands=['language'])
def lang(msg):
    try:
        languages[msg.chat.id]
    except KeyError:
        languages[msg.chat.id] = Language()
    keyboard = telebot.types.InlineKeyboardMarkup()
    eng = telebot.types.InlineKeyboardButton(text=languages[msg.chat.id]["English"] + "🇬🇧",
                                             callback_data="lang eng " + str(msg.from_user.id))
    rus = telebot.types.InlineKeyboardButton(text=languages[msg.chat.id]["Russian"] + '🇷🇺',
                                             callback_data="lang rus " + str(msg.from_user.id))
    ukr = telebot.types.InlineKeyboardButton(text=languages[msg.chat.id]["Ukrainian"] + "🇺🇦",
                                             callback_data="lang ukr " + str(msg.from_user.id))

    keyboard.add(eng)
    keyboard.add(rus)
    keyboard.add(ukr)
    bot_send_message(msg.chat.id, languages[msg.chat.id]["Choose language"], reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text and ("I like this expedition" in message.text
                                                            or 'I don`t like it' in message.text
                                                            or "Мне нравится эта экспедиция" in message.text
                                                            or "Мне она не нравится" in message.text
                                                            or "Мені подобається ця експедиція" in message.text
                                                            or "Мені вона не подобається" in message.text))
def get_vote(msg):
    if msg.from_user.id != msg.chat.id:
        return
    try:
        chat_id = chat_of_player[msg.from_user.id]
        if players_id[chat_id].state == 'vote':
            print(msg.text)
            print(chat_id)
            if not players_id[chat_id].cur_voting_for_exp[msg.from_user.id]:
                players_id[chat_id].cur_voting_for_exp[msg.from_user.id] = (1 if (msg.text.split()[1] == 'like' or msg.text.split()[1] == 'нравится' or msg.text.split()[1] == 'подобається') else -1)
                keyboard = telebot.types.ReplyKeyboardMarkup()
                bot_send_message(msg.chat.id, languages[chat_id]["You voted for this expedition"], reply_markup=None)
            sum = 0
            people_votes = ''
            for vote_i in players_id[chat_id].cur_voting_for_exp.values():
                if not vote_i:
                    return
                sum += int(vote_i)
            for player in players_id[chat_id].cur_voting_for_exp.keys():
                people_votes += '\n@' + str(bot.get_chat_member(chat_id, player).user.username) \
                                + ('👍' if players_id[chat_id].cur_voting_for_exp[player] == 1 else '👎🏿')
            bot_send_message(chat_id,
                             (languages[chat_id]['There will be such expedition'] if sum > 0 else languages[chat_id]['There won`t be such expedition']) +
                             people_votes)
            if sum > 0:
                players_id[chat_id].state = 'exp'
                players_id[chat_id].people_in_exp = dict()
                players_id[chat_id].kings_in_row = 0
                for id in players_id[chat_id].cur_exp:
                    players_id[chat_id].people_in_exp[id] = None
                gameplay.start_exp(players_id[chat_id].cur_exp, chat_id)
            else:
                players_id[chat_id].state = 'game'
                players_id[chat_id].king_rotation()
                players_id[chat_id].kings_in_row += 1
                if players_id[chat_id].kings_in_row == 5:
                    bot_send_message(chat_id, languages[chat_id]['RIP Avalon!!'])
                    string = ""
                    for item in players_id[chat_id].players.items():
                        string += '\n@' + bot.get_chat_member(chat_id, item[0]).user.username + languages[chat_id][' was '] + \
                                  ('❤️' if item[1] in tools.GameInfo.peaceful else '🖤') + item[1]
                    bot_send_message(chat_id, languages[chat_id]['Roles in this game:'] + string)
                    for id in players_id[chat_id].players:
                        chat_of_player.pop(id)
                    players_id.pop(chat_id)
                    return
                string = ''
                for i in range(0, len(players_id[chat_id].order)):
                    string += '\n' + str(i + 1) + '. @' \
                              + str(bot.get_chat_member(chat_id, players_id[chat_id].order[i]).user.username)
                    if i == players_id[chat_id].cur_king % len(players_id[chat_id].order):
                        string += '👑'
                    if players_id[chat_id].lady_lake and players_id[chat_id].lady_lake \
                            and i == players_id[chat_id].cur_lady % len(players_id[chat_id].order):
                        string += '👸'
                bot_send_message(chat_id, languages[chat_id]['Players order:'] + string)
                bot_send_message(chat_id, languages[chat_id]['New King is'] + ' @' +
                                 str(bot.get_chat_member(chat_id,
                                                         players_id[chat_id].order[
                                                             players_id[chat_id].cur_king]).user.username))
                if players_id[chat_id].kings_in_row == 4:
                    bot_send_message(chat_id, languages[chat_id]['Next skipped expedition will result into Avalon collapse!!!'])
                bot_send_message(chat_id, languages[chat_id]['This expedition is for '] +
                                 str(players_id[chat_id].exp_size[players_id[chat_id].get_num_of_exp()]) + languages[chat_id][' people'])

                players_id[chat_id].cur_exp = []
                for player in players_id[chat_id].players.keys():
                    players_id[chat_id].cur_voting_for_exp[player] = None
                vote.send_voting(chat_id, players_id[chat_id])
        else:
            bot.reply_to(msg, languages[chat_id]['No voting for expedition right now!'])

    except KeyError:
        print('bot durila')


@bot.message_handler(func=lambda message: message.text and ("Approve" in message.text
                                                            or 'Reject' in message.text
                                                            or "Поддержать" in message.text
                                                            or "Провалить" in message.text
                                                            or "Підтримати" in message.text
                                                            or "Провалити" in message.text))
def get_exp_choice(msg):
    if msg.from_user.id != msg.chat.id:
        return
    try:
        chat_id = chat_of_player[msg.from_user.id]
        if players_id[chat_id].state != 'exp':
            return
        if players_id[chat_id].people_in_exp[msg.from_user.id] is None:
            if players_id[chat_id].players[msg.from_user.id] in tools.GameInfo.peaceful and \
                    (msg.text.split()[1] == 'Reject' or msg.text.split()[1] == "Провалить" or msg.text.split()[1] == "Провалити"):
                bot.reply_to(msg, languages[chat_id]['You can`t do it due to your role'])
                return
            players_id[chat_id].people_in_exp[msg.from_user.id] = 1 if (msg.text.split()[1] == 'Approve' or msg.text.split()[1] == 'Поддержать' or msg.text.split()[1] == 'Підтримати') else 0
        sum = 0
        for choice in players_id[chat_id].people_in_exp.values():
            if choice is None:
                return
            sum += choice
        print(sum)
        num_of_exp = players_id[chat_id].successful_exp + players_id[chat_id].failed_exp
        exp_res = gameplay.exp_successful(sum, len(players_id[chat_id].people_in_exp),
                                          num_of_exp, len(players_id[chat_id].order))
        print(exp_res)
        if exp_res[0]:
            bot_send_message(chat_id, languages[chat_id]['Expedition was successful'] + '\n' + languages[chat_id]['Num of black cards is '] + str(exp_res[1]) + '\n\n' +
                             str(players_id[chat_id].successful_exp + 1) + languages[chat_id][' successful expeditions'] + '\n' +
                             str(players_id[chat_id].failed_exp) + languages[chat_id][' failed expeditions'])
            players_id[chat_id].successful_exp += 1
        else:
            bot_send_message(chat_id, languages[chat_id]['Expedition was failed'] + '\n' + languages[chat_id]['Num of black cards is '] + str(exp_res[1]) + '\n\n' +
                             str(players_id[chat_id].successful_exp) + languages[chat_id][' successful expeditions'] + '\n' +
                             str(players_id[chat_id].failed_exp + 1) + languages[chat_id][' failed expeditions'])
            players_id[chat_id].failed_exp += 1
        if players_id[chat_id].failed_exp == 3:
            bot_send_message(chat_id, languages[chat_id]['RIP Avalon!!'])
            string = ""
            for item in players_id[chat_id].players.items():
                string += '\n@' + bot.get_chat_member(chat_id, item[0]).user.username + languages[chat_id][' was '] + \
                          ('❤️' if item[1] in tools.GameInfo.peaceful else '🖤') + item[1]
            bot_send_message(chat_id, languages[chat_id]['Roles in this game:'] + string)
            for id in players_id[chat_id].players:
                chat_of_player.pop(id)
            players_id.pop(chat_id)
            return
        elif players_id[chat_id].successful_exp == 3:
            keyboard = telebot.types.InlineKeyboardMarkup()
            for id in players_id[chat_id].players:
                if players_id[chat_id].players[id] in tools.GameInfo.peaceful:
                    nickname = '@' + str(bot.get_chat_member(chat_id, id).user.username)
                    btn = telebot.types.InlineKeyboardButton(text=nickname,
                                                             callback_data='a' + nickname + ' ' + str(chat_id))
                    keyboard.add(btn)
            bot_send_message(chat_id, languages[chat_id]['Time to shot for Assassin'])
            for i in players_id[chat_id].players:
                if players_id[chat_id].players[i] == "Assassin":
                    bot_send_message(i, languages[chat_id]["Who do you want to kill?"], reply_markup=keyboard)

        else:
            players_id[chat_id].state = 'game'
            players_id[chat_id].king_rotation()
            string = ''
            for i in range(0, len(players_id[chat_id].order)):
                string += '\n' + str(i + 1) + '. @' \
                          + str(bot.get_chat_member(chat_id, players_id[chat_id].order[i]).user.username)
                if i == players_id[chat_id].cur_king % len(players_id[chat_id].order):
                    string += '👑'
                if players_id[chat_id].lady_lake and i == players_id[chat_id].cur_lady % len(players_id[chat_id].order):
                    string += '👸'
            bot_send_message(chat_id, languages[chat_id]['Players order:'] + string)
            bot_send_message(chat_id, languages[chat_id]['New King is'] + ' @' +
                             str(bot.get_chat_member(chat_id,
                                                     players_id[chat_id].order[
                                                         players_id[chat_id].cur_king]).user.username))
            bot_send_message(chat_id, languages[chat_id]['This expedition is for '] +
                             str(players_id[chat_id].exp_size[players_id[chat_id].get_num_of_exp()]) + languages[chat_id][' people'])
            if players_id[chat_id].get_num_of_exp() > 1 and players_id[chat_id].lady_lake and \
                    len(players_id[chat_id].checked) < len(players_id[chat_id].order):
                gameplay.lady_check(chat_id, players_id[chat_id])
                return

            players_id[chat_id].cur_exp = []
            for player in players_id[chat_id].players.keys():
                players_id[chat_id].cur_voting_for_exp[player] = None
            vote.send_voting(chat_id, players_id[chat_id])

    except KeyError:
        print('bot durila x2')


if __name__ == '__main__':
    bot.polling()
