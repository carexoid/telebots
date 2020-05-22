from enum import Enum


class DictSingletonMeta(type):

    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__()
        return cls._instance


class Dictionary(metaclass=DictSingletonMeta):
    _dictionary = {
                    "You don`t take part in any game": ["You don`t take part in any game", 'Вы не принимаете участие ни в одной из игр', 'Ви не берете участь у жодній грі'],
                   'You have left the game': ['You have left the game', 'Вы вышли из игры', 'Ви вийшли з гри'],
                   'Merlin has left the game': ['Merlin has left the game', 'Мерлин вышел из игры', 'Мерлін вийшов з гри'],
                   'RIP Avalon!!': ['RIP Avalon!!', 'RIP Авалон!!', 'RIP Авалон!'],
                   'Roles in this game:': ['Roles in this game:', 'Роли в игре:', 'Ролі у грі:'],
                   "You are the new Assassin": ["You are the new Assassin", 'Вы новый Ассасин', 'Ви новий Ассасін'],
                   "All players have left the game": ["All players have left the game", 'Все игроки вышли из игры', 'Усі гравці вийшли з гри'],
                   'Game aborted': ['Game aborted', 'Игра отменена', 'Гра скасована'],
                   'Registration is on': ['Registration is on', 'Идёт регистрация', 'Триває реєстрація'],
                   'Players in game:': ['Players in game:', 'Игроки:', 'Гравці:'],
                   "Register": ["Register", "Регистрация", "Реєстрація"],
                   'You`re creator of game in chat ': ['You`re creator of game in chat ', 'Вы создатель игры в чате ', 'Ви редактор гри у чаті '],
                   'Only you can launch the game': ['Only you can launch the game', 'Только вы можете настраивать игру', 'Лише ви можете налаштовувати гру'],
                   'To be able to register in game, '
                   'say /start to @Avalon117bot in private messages '
                   'and push registration button again'
                                            : ['To be able to register in game, '
                                          'say /start to @Avalon117bot in private messages '
                                          'and push registration button again', 'Что бы зарегестрироваться, ' 'напишите /start в сообщения' '@Avalon117bot', 'Щоб зареєструватись, ' 'напишіть /start у привітні повідомлення ' '@Avalon117bot'],
                   'Game': ['Game', 'Игра', 'Гра'],
                   'Registration': ['Registration', 'Регистрация', 'Реєстрація'],
                   ' is on!': [' is on!', 'идёт!' 'триває!'],
                   'No registration started!': ['No registration started!', 'Сейчас нет регистрации!', 'Регістрація не розпочата!'],
                   'Run /start_registration': ['Run /start_registration', 'Начать /start_registration', 'Розпочати /start_registration'],
                   'Game is on!': ['Game is on!', 'Игра идёт!', 'Гра триває!'],
                   "You have launched the game in": ["You have launched the game in", 'Ты присоединился к игре ', 'Ти приєднався до гри '],
                   'Players order:': ['Players order:', 'Порядок игроков:', 'Порядок гравців:'],
                   "King is": ["King is", 'Король – ', 'Король – '],
                   "Lady of the Lake is": ["Lady of the Lake is", 'Леди Озеро – ', 'Леді Озеро - '],
                   'You`re not creator of this game!': ['You`re not creator of this game!', 'Ты не создатель игры!', 'Ти не створював цю гру!'],
                   'Wrong number of players to start, this game is for 5 - 10 players':
                       ['Wrong number of players to start, this game is for 5 - 10 players',
                        'Невозможное количество игроков, нужно 5-10', 'Неможлива кількість гравців, потрібно 5-10'],
                   "The game has already started": ["The game has already started", 'Игра уже началась', 'Гра вже почалась'],
                   "Morgana, a minion of Mordred, deceives Percival. During the beginning round where "
                   "Merlin puts his "
                   "thumb in the air to reveal himself to Percival, Morgana also raises her own thumb, "
                   "confusing Percival as to which 'Merlin' to trust."
                   : ["Morgana, a minion of Mordred, deceives Percival. During the beginning round where "
                             "Merlin puts his "
                             "thumb in the air to reveal himself to Percival, Morgana also raises her own thumb, "
                             "confusing Percival as to which 'Merlin' to trust.",
                              "Моргана, союзник Мордреда, путает Персиваля. В начале игры "
                              "Мерлин показывает свой" " большой палец вверх, чтобы познакомить с собой Персиваля, и в то же время Моргана показывает свой, "
                              "путая Персиваля, чтобы он не знал, кому из 'Мерлинов' доверять.",
                              "Моргана, союзник Мордреда, плутає Персиваля. На початку гри " 
                              "Мерлін показує свій" 
                              " великий палець вгору, щоб познайомити з собою Персиваля, і в той же час Моргана показує свій, "
                              "плутаючи Персиваля, щоб він не знав, кому з 'Мерлінів' можна довіряти."],
                   "Oberon despite being a servant of Mordred, is somewhat of "
                   "a hindrance. Oberon does not reveal himself to evil players, and also they do not reveal "
                   "themselves to him. Oberon still raises his thumb for Merlin to see, however."
                   : ["Oberon despite being a servant of Mordred, is somewhat of "
                             "a hindrance. Oberon does not reveal himself to evil players, and also they do not reveal "
                             "themselves to him. Oberon still raises his thumb for Merlin to  see, however.",
                           "Оберон, хотя и является союником Мордреда, в определённой степени является " 
                            "проблемой. Оберон не открывает себя другим союзникам Мордреда, так же они не открываются "
                             "для него. Однако, не смотря на это, всё же показывает свою сторону Мерлину.",
                            "Оберон, попри те, що є союзником Мордреда, певною мірою є " 
                            "проблемою. Оберон не показує себе іншим союзникам Мордреда, так само вони не відкриваються "
                             "для нього. Але, не дивлячись на це, все ще показує свою сторону Мерліну."],
                   "Mordred helps the evil side because Merlin does not know his identity. As Mordred, "
                   "it is imperative that you recognize your unique situation because you "
                   'will be able to watch the votes to see how everyone votes for teams to which the other '
                   'minions belong.'
                   : ["Mordred helps the evil side because Merlin does not know his identity. As Mordred, "
                             "it is imperative that you recognize your unique situation because you "
                             'will be able to watch the votes to see how everyone votes for teams to which the other '
                             'minions belong.',
                             "Мордред помогает тёмной стороне, ведь Мерлин не знает о нём. Будучи Мордредом, "
                             "важно анализировать игру и экспедиции, ведь вы можете пользоваться тем, "
                             'что Мерлин не знает, чьим союзником '
                             'вы являетесь.',
                             "Мордред допамагає темній стороні, адже Мерлін не знає про нього. Будучи Мордредом,  "
                             "важливо аналізувати гру та експедиції, адже ви можете користуватись тим, "
                             'що Мерлін не знає, на якій стороні '
                             'ви граєте'],
                   "What role do you want to add?": ["What role do you want to add?", "Какую роль вы хотите добавить?", "Яку роль ви хочете додати?"],
                   "Mordred wins": ["Mordred wins"],
                   "Your telegram account has no username": ["Your telegram account has no username"],
                   'You are in not ended game!': ['You are in not ended game!', 'Ты в незаконченной игре!', 'Гра з тобою ще не закінчилась!'],
                   'You`re registered for the Avalon game in ': ['You`re registered for the Avalon game in ', 'Вы зарегестрировались для игры в Авалон в ', 'Ви зареєструвались для гри в Авалон в '],
                   'Wrong number of expeditors': ['Wrong number of expeditors', 'Неправильное количество людей в экспедиции', 'Неправильна кількість людей в експедиції'],
                   "The expedition is:": ["The expedition is:", 'Экспедиция:', "Експедиція:"],
                   "Lady of the Lake has checked": ["Lady of the Lake has checked", "Леди Озеро проверила", "Леді Озеро перевірила"],
                   " is servant of Arthur": [" is servant of Arthur", " — союзник Артура", " — союзник Артура"],
                   " is servant of Mordred": [" is servant of Mordred", " — союзник Мордреда", " — союзник Мордреда"],
                   " is new Lady of the Lake": [" is new Lady of the Lake", " новая Леди Озеро", "нова Леді Озеро"],
                   "Don`t touch old buttons, run /start_registration first!": ["Don`t touch old buttons, run /start_registration first!", "Не нажимай старые кнопки, напиши /start_registration для начала!", "Не натискай старі кнопки, почни з /start_registration!"],
                   'No game to be aborted': ['No game to be aborted', 'Нет игры для отмены', 'Немає гри для скасування'],
                   "I like this expedition": ["I like this expedition", "Мне нравится эта экспедиция", "Мені подобається ця експедиція"],
                   'I don`t like it': ["I don`t like it", "Мне она не нравится", "Мені вона не подобається"],
                   "You voted for this expedition": ["You voted for this expedition", "Ты проголосовал за эту экспедицию", "Ти проголосував за цю експедицію"],
                   'There will be such expedition': ['There will be such expedition', 'Экспедиция состоится', 'Експедиція відбудеться'],
                   'There won`t be such expedition': ['There won`t be such expedition', 'Экспедиция не состоится', 'Експедиція не відбудеться'],
                   'New King is': ['New King is', 'Новый Король — ', 'Новий Король — '],
                   'Next skipped expedition will result into Avalon collapse!!!': ['Next skipped expedition will result into Avalon collapse!!!', 'Следующая пропущенная экспедиция — Авалон падёт!', 'Наступна скасована експедиція — Авалон паде!'],
                   'No voting for expedition right now!': ['No voting for expedition right now!', 'Сейчас не голосуют за экспедицию!', 'Зараз не голосують за експедицію!'],
                   "Approve": ["Approve", "Поддержать", "Підтримати"],
                   'Reject': ['Reject', "Провалить", "Провалити"],
                   'You can`t do it due to your role': ['You can`t do it due to your role', 'Вы не можете делать это в соответствии с ролью', 'Ви не можете робити це у зв`язку з роллю'],
                   'Expedition was successful': ['Expedition was successful', 'Экспедиция прошла успешно', 'Експедиція пройшла успішно'],
                   'Num of black cards is ': ['Num of black cards is ', 'Количество черных карт — ', 'Кількість чорних карток — '],
                   ' successful expeditions': [' successful expeditions', ' успешных экспедиций', 'вдалих експедицій'],
                   ' failed expeditions': [' failed expeditions', ' проваленных экспедиций', ' провалених експедицій'],
                   'Expedition was failed': ['Expedition was failed', "Экспедиция провалена", "Екапедиція провлена"],
                   ' was ': [' was '],
                   'Time to shot for Assassin': ['Time to shot for Assassin', "Время для выстрела Ассасина", "Час для вистрілу Асасіна"],
                   "Who do you want to kill?": ["Who do you want to kill?", "Кого вы хотите убить?", "Кого ви хочете вбити?"],
                   'This expedition is for ': ['This expedition is for ', "Это экспедиция для", "Ця експедиція для "],
                   ' people': [' people', " человек", " людей"],
                   'You are a loyal servant of King Arthur, so your main goal is complete the missions'
                                : ['You are a loyal servant of King Arthur, so your main goal is complete the missions',
                                   "Вы — союзник Короля Артура, ваша главная цель — успешно закончить экспедиции",
                                   "Ви — союзник Короля Артура, ваша головна мета — вдало закінчити експедиції"],
                   "Merlin learns Mordred's followers when the game begins. Merlin must steer the knights correctly "
                   "without it being obvious they know who all the minions are, which means they must make deductions "
                   "based on actions taken by players in the game."
                                : ["Merlin learns Mordred's followers when the game begins. Merlin must steer the knights correctly "
                                  "without it being obvious they know who all the minions are, which means they must make deductions "
                                  "based on actions taken by players in the game.",
                                "Мерлин узнаёт всех всех союзников Мордреда в начале игры. Мерлин должен делать выбор аккуратно, "
                                  "чтобы не показывать прямо того, что знает, кто на чьей стороне, ведь в конце союзники Мордреда делают выбор, "
                                  "который обосновывается действиями других игроков.",
                                "Мерлін знає усіх союзників Мордреда з початку гри. Мерлін має грати дуже обережно, "
                                  "щоб не показувати прямо, що знає, хто на чиїй стороні, адже в кінці союзники Мордреда роблять вибір, "
                                  "який базується на діях інших гравців."],
                   "Percival, a loyal servant of Arthur, is able to learn Merlin's identity at the beginning of the "
                   "game by having Merlin stick his thumb in the air. Merlin—and everyone else—does not learn "
                   "Percival's identity. This character can help cover for Merlin and will balance the game towards "
                   "the good team."
                               : ["Percival, a loyal servant of Arthur, is able to learn Merlin's identity at the beginning of the "
                                "game by having Merlin stick his thumb in the air. Merlin—and everyone else—does not learn "
                                "Percival's identity. This character can help cover for Merlin and will balance the game towards "
                                "the good team.",
                               "Персиваль, союзник Артура, с самого начала может узнать Мерлина, увидив "
                                "его поднятый вверх палец. Мерлин, как и все остальные, не знают "
                                "личность Персиваля. Этот персонаж может отвести подозрения от Мерлина и добавляет баланс "
                                "доброй стороне.",
                              "Персиваль, союзник Артура, з самого початку може дізнатись, хто Мерлін, побачивши "
                                "його піднятий вгору палець. Мерлін, як і будь-який інший гравець, не знають, "
                                "хто є Персивалем. Цей персонаж може відвести підозру від Мерліна та додає баланс "
                                "добрій стороні."],
                   'Just an ordinary servants of Mordred who wants to fail missions'
                               : ['Just an ordinary servants of Mordred who wants to fail missions',
                                  "Просто союзник Мордреда, который хочет завалить экспедиции",
                                  "Просто союзник Мордреду, який хоче завалити експедиції"],
                   "Morgana, a minion of Mordred, deceives Percival. During the beginning round where Merlin puts his "
                   "thumb in the air to reveal himself to Percival, Morgana also raises her own thumb, "
                   "confusing Percival as to which 'Merlin' to trust. Morgana balances the game in favor of evil, "
                   "and her effect of course only works when Percival's ability is agreed to be used."
                               : ["Morgana, a minion of Mordred, deceives Percival. During the beginning round where Merlin puts his "
                               "thumb in the air to reveal himself to Percival, Morgana also raises her own thumb, "
                               "confusing Percival as to which 'Merlin' to trust. Morgana balances the game in favor of evil, "
                               "and her effect of course only works when Percival's ability is agreed to be used.",
                                  "Моргана, союзник Мордреда, путает Персиваля. В начале игры " 
                                  "Мерлин показывает свой"
                                  " большой палец вверх, чтобы познакомить с собой Персиваля, и в то же время Моргана показывает свой, " 
                                  "путая Персиваля, чтобы он не знал, кому из 'Мерлинов' доверять. Моргана усиляет темную сторону",
                                  "Моргана, союзник Мордреда, плутає Персиваля. На початку гри " 
                                  "Мерлін показує свій" 
                                  " великий палець вгору, щоб познайомити з собою Персиваля, і в той же час Моргана показує свій, "
                                  "плутаючи Персиваля, щоб він не знав, кому з 'Мерлінів' можна довіряти. Моргана посилює темну сторону"],
                   "Unlucky you. You've drawn the Oberon card, who despite being a servant of Mordred, is somewhat of "
                   "a hindrance. Oberon does not reveal himself to evil players, and also they do not reveal "
                   "themselves to him. Oberon still raises his thumb for Merlin to see, however. Oberon makes the "
                   "other evil players have to deduce one of their own's identity, while Oberon does the same with "
                   "them."
                               : ["Unlucky you. You've drawn the Oberon card, who despite being a servant of Mordred, is somewhat of "
                              "a hindrance. Oberon does not reveal himself to evil players, and also they do not reveal "
                              "themselves to him. Oberon still raises his thumb for Merlin to see, however. Oberon makes the "
                              "other evil players have to deduce one of their own's identity, while Oberon does the same with "
                              "them.",
                               "Невезуха... Ты достал карту Оберона, что означает союз с Мордредом, но в качестве "
                              "обузы. О нём не знают другие союзники Мордреда, как и он не знает их. "
                              "Оберон показывает свой палец вверх и открывает сторону Мерлину. Оберону стоит "
                              "узнать других тёмных игроков и показать, что тоже играет на их"
                              "стороне.",
                               "Яка невдача... Тобі дісталась картка Оберона, що означає союз з Мордредом, але у якості певної"
                              "обузи. Оберон не показує себе іншим темним гравцям та не знає своїх союзників "
                              "також. Оберон все одно показує свою сторону Мерліну. Оберону варто "
                              "зрозуміти інших темних гравців та показати, що він також грає на їхній"
                              "стороні."],
                   'Mordred helps the evil side because Merlin does not know his identity, but hurts in their ability '
                   'to detect Merlin because he can`t always vote correctly anymore.  Basically, adding him helps '
                   'them win more often by just causing 3 missions to fail, but makes it harder to assassinate Merlin '
                   'in the end.  As Mordred, it is imperative that you recognize your unique situation because you '
                   'will be able to watch the votes to see how everyone votes for teams to which the other minions '
                   'belong.'
                               : ['Mordred helps the evil side because Merlin does not know his identity, but hurts in their ability '
                               'to detect Merlin because he can`t always vote correctly anymore.  Basically, adding him helps '
                               'them win more often by just causing 3 missions to fail, but makes it harder to assassinate Merlin '
                               'in the end.  As Mordred, it is imperative that you recognize your unique situation because you '
                               'will be able to watch the votes to see how everyone votes for teams to which the other minions '
                               'belong.',
                                "Мордред помогает тёмной стороне, ведь Мерлин не знает о нём, но наличие "
                                "этой роли усложняет процесс вычисления Мерлина, поскольку второй не может"
                                " больше голосовать всегда правильно."
                                " Обычно, добавления Мордреда помогает темней стороне выигрывать чаще просто провалив"
                                " 3 експедиции, но при этом усложняет процесс вычисления Мерлина."
                                " Будучи Мордредом, "
                             "важно анализировать игру и экспедиции, ведь вы можете пользоваться тем, "
                             'что Мерлин не знает, чьим союзником '
                             'вы являетесь.',
                             "Мордред допамагає темній стороні, адже Мерлін не знає про нього, але наявність цієї ролі "
                             "поскладнює процес пошуку Мерліна, адже останній більше не може завжди голосувати вірно. "
                             "Зазвичай, додання Мордреда допомагає темній стороні перемагати частіше просто заваливши 3 "
                             "експедиції але при цьому поскладнює процес пошуку Мерліна. Будучи Мордредом,  "
                             "важливо аналізувати гру та експедиції, адже ви можете користуватись тим, "
                             'що Мерлін не знає, на якій стороні '
                             'ви граєте'],
                   'Assassin is a minion of Mordred who wants to find Merlin. Merlin votes correctly pretty much '
                   'always so the assassin`s most important task is watching the '
                   'voting to see who is able to do that.  When you know the players in the game, you can often tell '
                   'who knows too much, but when you do not, you often have to look to the voting results to deduce '
                   'who is Merlin. '
                               : ['Assassin is a minion of Mordred who wants to find Merlin. Merlin votes correctly pretty much '
                               'always so the assassin`s most important task is watching the '
                               'voting to see who is able to do that.  When you know the players in the game, you can often tell '
                               'who knows too much, but when you do not, you often have to look to the voting results to deduce '
                               'who is Merlin. ',

                             "Ассасин — союзник Мордреда, который хочет найти Мерлина. Выборы Мерлина слишком правильные"
                            "всегда, так что наиболее важной задачей ассасина является"
                            "внимательная слежка за экспедициями чтобы понять, кто это может быть." 
                            "Когда вы следите за словами игроков, то точно можете сказать, кто знает слишком много, "
                            "но если что-то упустили, стоит смотреть и за результатами голосований чтобы выяснить,"
                            "кто является Мерлином. ",

                            "Асасін — союзник Мордреда, який бажає знайти Мерліна. Вибори Мерліна занадто правильні"
                            "завжди, тому найважливішою задачею асасіна є уважне спостерігання "
                            "за експедиціями щоб зрозуміти, хто це може бути."
                            "Коли ви слідкуєте за словами гравців, то точно можете сказати, хто знає занадто багато, "
                            "але якщо ви щось пропустили, варто дивитись і за результатами голосувань, щоб вияснити,"
                            "хто є Мерліном"],
                   "Your role is ": ["Your role is ", "Ваша роль — ", "Ваша роль — "],
                   ' is minion of Mordred': [' is minion of Mordred'],
                   'Minions of Mordred are:': ['Minions of Mordred are:'],
                   'Your teammates are:': ['Your teammates are:', "Ваша команда:", "Ваша команда:"],
                   'Merlin is one of them:': ['Merlin is one of them:', "Мерлин один из них:", "Мерлін один з них:"],
                   'Do you like this expedition?': ['Do you like this expedition?', "Вам нравится эта экспедиция?", "Вам подобається ця експедиція?"],
                   'Your choice in expedition?': ['Your choice in expedition?', "Ваш выбор в экспедиции?", "Ваш вибір в експедиції?"],
                   "It is time for Lady of the Lake to check.": ["It is time for Lady of the Lake to check.", "Время проверки Леди Озеро.", "Час перевірки Леді Озеро."],
                   "Who do you want to check?": ["Who do you want to check?", "Кого вы хотите проверить?", "Кого вр хочете перевірити?"],
                   'Merlin was killed': ['Merlin was killed', "Мерлин убит", "Мерлін вбитий"],
                   'Merlin is alive!': ['Merlin is alive!', "Мерлин живой!", "Мерлін живий!"],
                   ' was killed': [' was killed', " был убит", " вбитий"],
                   "Morgana": ["Morgana", "Моргана", "Моргана"],
                   "Mordred": ["Mordred", "Мордред", "Мордред"],
                   "Oberon": ["Oberon", "Оберон", "Оберон"],
                   "Lady of the Lake": ["Lady of the Lake", "Леди Озеро", "Леді Озеро"],
                   "Choose expeditors": ["Choose expeditors", "Выберите, кто пойдет в экспедицию", "Оберіть, хто піде в експедицію"],
                   "Send expedition": ["Send expedition", "Отправить экспедицию", "Відправити експецидію"],
                   "Send": ["Send", "Отправить", "Відправити"],
                   " has been removed": [" has been removed", " был удален", " видалений"],
                   " has been added": [" has been added", " был добавлен", " доданий"],
                   "Choose language": ["Choose language", "Выберите язык", "Оберіть мову"],
                   "English": ["English", "Английский", "Англійська"],
                   "Russian": ["Russian", "Русский", "Російська"],
                   "Ukrainian": ["Ukrainian", "Украинский", "Українська"],
                   'like': ['like', 'нравится', 'подобається']

                  }


    def get(self, key, index) -> str:
        try:
            return self._dictionary[key][index]
        except IndexError:
            return self._dictionary[key][0]


class State(Enum):
    eng = 0
    rus = 1
    ukr = 2


class Language:
    def __init__(self, state=0):
        self._state = state
        self._dictionary = Dictionary()
        print(self._state)

    def __getitem__(self, item):
        return self._dictionary.get(item, self._state)

    def set_lang(self, lang: State):
        if lang is State.eng:
            self._state = 0
        elif lang is State.rus:
            self._state = 1
        elif lang is State.ukr:
            self._state = 2

        print('dasffdg')



