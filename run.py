import telebot
import config
import time
import logging
import json
from db_tool import DbQuery

db_query = DbQuery()
bot = telebot.TeleBot(config.token)
logging.basicConfig(filename="sample.log", level=logging.INFO)

markup = telebot.types.InlineKeyboardMarkup()
markup.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
           telebot.types.InlineKeyboardButton('2', callback_data='2'),
           telebot.types.InlineKeyboardButton('3', callback_data='3'),
           telebot.types.InlineKeyboardButton('4', callback_data='4'),
           telebot.types.InlineKeyboardButton('5', callback_data='5'))

def add_new_polling(message_id):
    query = """SELECT *
        	        FROM public.polls
                    WHERE id={};"""
    query_result = db_query.execute_query(query.format(message_id))
    if len(query_result.value) < 1:
        query = """INSERT INTO public.polls
                    (id, votes)
	         VALUES ({}, 0);"""
        query_result = db_query.execute_query(query.format(message_id), is_dml=True)
        add_vote(message_id,0)
        add_new_polling(message_id)
    else:
        return query_result.value[0][1]

def add_vote(message_id,votes):
    query = """UPDATE public.polls
	            SET votes={}
	            WHERE id={};"""
    query_result = db_query.execute_query(query.format(int(votes)+1,message_id), is_dml=True)

@bot.message_handler(regexp="/test")
def test(message):
    bot.send_message(message.chat.id, 0,reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data:
            # bot.answer_callback_query(call.id, text="Done!")
            votes = add_new_polling(call.message.message_id)
            try:
                summa = float(call.message.text)*int(votes)
            except:
                summa = 0
            try:
                add_vote(call.message.message_id, votes)
            except:
                add_vote(call.message.message_id, 0)
            votes = add_new_polling(call.message.message_id)
            bot.edit_message_text(str((summa+int(call.data))/int(votes)),call.message.chat.id,call.message.message_id, reply_markup=markup)
            bot.answer_callback_query(call.id, text=str(call.data))
    pass
            # bot.send_message(call.data, call.message.chat.username'test')
            # for data in call.message.entities[1]:
            #     print((data))

@bot.message_handler(content_types='text')
def default_answer(message):
    # bot.send_message(message.chat.id, "You are not authorized")
    pass



while True:
    bot.polling(none_stop=True)
    # try:
    #     bot.polling(none_stop=True)
    # except Exception as e:
    #     logging.error(e)
    #     time.sleep(15)