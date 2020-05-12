import teletoken
import telebot

bot = telebot.TeleBot(teletoken.token)


def bot_send_message(chat_id, text, parse_mode=None, disable_web_page_preview=None,
                     disable_notification=False, reply_to_message_id=None, reply_markup=None, timeout=None, **kwargs):
    try:
        msg = bot.send_message(chat_id, text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview,
                         disable_notification=disable_notification, timeout=timeout,
                         reply_to_message_id=reply_to_message_id,
                         reply_markup=reply_markup, **kwargs)
        return msg
    except telebot.apihelper.ApiException:
        return