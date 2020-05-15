import random
import telebot
import tools

from setup import bot, bot_send_message

botbot = bot


def shuffle_roles(size, additional):
    roles = []

    if size == 1: roles = ['Merlin']

    if size == 2: roles = ['Assassin', 'Minion of Mordred']

    if size == 5:
        roles = ['Loyal Servant of Arthur', 'Merlin', 'Percival',
                 'Assassin']
    elif size == 6:
        roles = ['Loyal Servant of Arthur', 'Loyal Servant of Arthur', 'Merlin', 'Percival',
                 'Assassin']
    elif size == 7:
        roles = ['Loyal Servant of Arthur', 'Loyal Servant of Arthur', 'Merlin', 'Percival',
                 'Assassin']
    elif size == 8:
        roles = ['Loyal Servant of Arthur', 'Loyal Servant of Arthur', 'Loyal Servant of Arthur', 'Merlin', 'Percival',
                 'Assassin']
    elif size == 9:
        roles = ['Loyal Servant of Arthur', 'Loyal Servant of Arthur', 'Loyal Servant of Arthur',
                 'Loyal Servant of Arthur', 'Merlin', 'Percival', 'Assassin']
    elif size == 10:
        roles = ['Loyal Servant of Arthur', 'Loyal Servant of Arthur', 'Loyal Servant of Arthur',
                 'Loyal Servant of Arthur', 'Merlin', 'Percival', 'Assassin']

    for key in additional:
        if additional[key] and len(roles) <= size:
            roles.append(key)

    while len(roles) < size:
        roles.append('Minion of Mordred')

    random.shuffle(roles)
    return roles


def make_roles(roles, additional):
    roles_list = shuffle_roles(len(roles), additional)
    index = 0
    roles_description = {
        'Loyal Servant of Arthur': 'You are a loyal servant of King Arthur, so your main goal is complete the missions',
        'Merlin': "Merlin learns Mordred's followers when the game begins. Merlin must steer the knights correctly "
                  "without it being obvious they know who all the minions are, which means they must make deductions "
                  "based on actions taken by players in the game.",
        'Percival': "Percival, a loyal servant of Arthur, is able to learn Merlin's identity at the beginning of the "
                    "game by having Merlin stick his thumb in the air. Merlin—and everyone else—does not learn "
                    "Percival's identity. This character can help cover for Merlin and will balance the game towards "
                    "the good team.",
        'Minion of Mordred': 'Just an ordinary servants of Mordred who wants to fail missions',
        'Morgana': "Morgana, a minion of Mordred, deceives Percival. During the beginning round where Merlin puts his "
                   "thumb in the air to reveal himself to Percival, Morgana also raises her own thumb, "
                   "confusing Percival as to which 'Merlin' to trust. Morgana balances the game in favor of evil, "
                   "and her effect of course only works when Percival's ability is agreed to be used.",
        'Oberon': "Unlucky you. You've drawn the Oberon card, who despite being a servant of Mordred, is somewhat of "
                  "a hindrance. Oberon does not reveal himself to evil players, and also they do not reveal "
                  "themselves to him. Oberon still raises his thumb for Merlin to see, however. Oberon makes the "
                  "other evil players have to deduce one of their own's identity, while Oberon does the same with "
                  "them.",
        'Mordred': 'Mordred helps the evil side because Merlin does not know his identity, but hurts in their ability '
                   'to detect Merlin because he can’t always vote correctly anymore.  Basically, adding him helps '
                   'them win more often by just causing 3 missions to fail, but makes it harder to assassinate Merlin '
                   'in the end.  As Mordred, it is imperative that you recognize your unique situation because you '
                   'will be able to watch the votes to see how everyone votes for teams to which the other minions '
                   'belong.',
        'Assassin': 'Assassin is a minion of Mordred who wants to find Merlin. Merlin votes correctly pretty much '
                    'always so the assassin’s most important task is watching the '
                    'voting to see who is able to do that.  When you know the players in the game, you can often tell '
                    'who knows too much, but when you do not, you often have to look to the voting results to deduce '
                    'who is Merlin. '
    }
    for key in roles:
        roles[key] = roles_list[index]
        index = index + 1
    for key in roles:
        send_text = "Your role is " + roles[key]
        bot_send_message(key, send_text)
        bot_send_message(key, roles_description[roles[key]])
        teamlist = ''
        mordred = ''
        oberon = ''
        if (roles[key] not in tools.GameInfo.peaceful and roles[key] != 'Oberon') or roles[key] == 'Merlin':
            for teammate_key in roles.keys():
                if roles[teammate_key] == 'Mordred':
                    mordred = '\n@' + botbot.get_chat_member(teammate_key, teammate_key).user.username + \
                              ' is minion of Mordred'
                if roles[teammate_key] == 'Oberon':
                    oberon = '\n@' + botbot.get_chat_member(teammate_key, teammate_key).user.username + \
                             ' is minion of Mordred'
                if roles[teammate_key] not in tools.GameInfo.peaceful and roles[teammate_key] != 'Oberon' \
                        and roles[teammate_key] != 'Mordred':
                    teamlist += '\n@' + botbot.get_chat_member(teammate_key, teammate_key).user.username + \
                                ' is minion of Mordred'
            bot_send_message(key, ('Minions of Mordred are:' + oberon if roles[key] == 'Merlin'
                                   else 'Your teammates are:' + mordred) + teamlist)
        if roles[key] == 'Percival':
            for teammate_key in roles.keys():
                if roles[teammate_key] == 'Merlin' or roles[teammate_key] == 'Morgana':
                    teamlist += '\n@' + botbot.get_chat_member(teammate_key, teammate_key).user.username
            bot_send_message(key, 'Merlin is one of them:' + teamlist)

    return roles
