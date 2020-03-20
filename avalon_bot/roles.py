import random
import telebot
import teletoken

bot = telebot.TeleBot(teletoken.token)


def shuffle_roles(size, additional):
    roles = []
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
        if additional[key]:
            roles.append(key)

    while len(roles) < size:
        roles.append('Minion of Mordred')

    if len(roles) > size:
        print('ERROR')
        # TODO error catch

    random.shuffle(roles)
    return roles


def make_roles(roles, additional):
    roles_list = shuffle_roles(len(roles), additional)
    index = 0
    roles_description = {
        'Loyal Servant of Arthur': '1',
        'Merlin': '2',
        'Percival': "Percival, a loyal servant of Arthur, is able to learn Merlin's identity at the beginning of the "
                    "game by having Merlin stick his thumb in the air. Merlin—and everyone else—does not learn "
                    "Percival's identity. This character can help cover for Merlin and will balance the game towards "
                    "the good team.",
        'Minion of Mordred': '4',
        'Morgana': "Morgana, a minion of Mordred, deceives Percival. During the beginning round where Merlin puts his "
                   "thumb in the air to reveal himself to Percival, Morgana also raises her own thumb, "
                   "confusing Percival as to which 'Merlin' to trust. Morgana balances the game in favor of evil, "
                   "and her effect of course only works when Percival's ability is agreed to be used.",
        'Oberon': "Unlucky you. You've drawn the Oberon card, who despite being a servant of Mordred, is somewhat of "
                  "a hindrance. Oberon does not reveal himself to evil players, and also they do not reveal "
                  "themselves to him. Oberon still raises his thumb for Merlin to see, however. Oberon makes the "
                  "other evil players have to deduce one of their own's identity, while Oberon does the same with "
                  "them.",
        'Mordred': '7'
    }
    for key in roles:
        roles[key] = roles_list[index]
        index = index + 1
    for key in roles:
        send_text = "Your role is " + roles[key]
        bot.send_message(key, send_text)
        bot.send_message(key, roles_description[roles[key]])
    return roles
