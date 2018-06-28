import telebot
import config
import time
import logging
import json
from db_tool import DbQuery

db_query = DbQuery()
bot = telebot.TeleBot(config.token)
logging.basicConfig(filename="sample.log", level=logging.INFO)

@bot.message_handler(regexp="/test")
def test(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton('+1', callback_data=message.chat.id))
    bot.send_message(message.chat.id, 0,reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data:
            bot.answer_callback_query(call.id, text="Done!")
            bot.edit_message_text(call.message.text+1,call.message.chat.id,call.message.id)
            bot.answer_callback_query(call.id, text="+1")
    pass
            # bot.send_message(call.data, call.message.chat.username'test')
            # for data in call.message.entities[1]:
            #     print((data))


while True:
    bot.polling(none_stop=True)
    # try:
    #     bot.polling(none_stop=True)
    # except Exception as e:
    #     logging.error(e)
    #     time.sleep(15)