import telebot
import config
import time
import logging
import json
from db_tool import DbQuery
from openpyxl import Workbook


db_query = DbQuery()
bot = telebot.TeleBot(config.token)
logging.basicConfig(filename="sample.log", level=logging.INFO)

markup = telebot.types.InlineKeyboardMarkup()
markup.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
           telebot.types.InlineKeyboardButton('2', callback_data='2'),
           telebot.types.InlineKeyboardButton('3', callback_data='3'))

def add_new_polling(chat_id,message_id,message_text):
    query = """SELECT *
        	        FROM public.polls
                    WHERE msg_id={};"""
    query_result = db_query.execute_query(query.format(message_id))
    if len(query_result.value) < 1:
        query = """INSERT INTO public.polls
                    (chat_id, msg_id,votes,sum,text)
	         VALUES ({}, {},0,0,'{}');"""
        query_result = db_query.execute_query(query.format(chat_id, message_id,message_text), is_dml=True)
        create_user_list(message_id)
        add_new_polling(chat_id,message_id,message_text)
    else:
        return query_result.value

def create_user_list(message_id):
   query = """CREATE TABLE public."{}"
            (user_id integer NOT NULL)
            WITH (
            OIDS = FALSE
            )
            TABLESPACE pg_default;
            ALTER TABLE public."{}"
            OWNER to root;"""
   query_result = db_query.execute_query(query.format(message_id,message_id), is_dml=True)
   print('CREATE USER LIST')
   print(query_result.success)

def user_is_new(message_id,user_id):
    query = """SELECT *
            	        FROM public."{}"
                        WHERE user_id={};"""
    query_result = db_query.execute_query(query.format(message_id,user_id))
    if len(query_result.value) < 1:
        query = """INSERT INTO public."{}"
                        (user_id)
    	         VALUES ({});"""
        query_result = db_query.execute_query(query.format(message_id,user_id), is_dml=True)
        return True
    else:
        return False

def add_vote(message_id,votes):
    query = """UPDATE public.polls
	            SET votes={}
	            WHERE msg_id={};"""
    query_result = db_query.execute_query(query.format(int(votes)+1,message_id), is_dml=True)

def new_sum(message_id,new_summa):
    query = """UPDATE public.polls
    	            SET sum={}
    	            WHERE msg_id={};"""
    query_result = db_query.execute_query(query.format(new_summa, message_id), is_dml=True)


@bot.message_handler(regexp="/test")
def test(message):
    questions = ["Мне понятна цель и задачи, которые стоят перед проектом со стороны Яндекс Такси",
                 "Роли участников проектной команды распределены, не дублируются и работа ведется в соответствии с этими ролями",
                 "У участников проекта есть понятные роли, они не дублируется и непокрытых зон также нет"]
    for msg in questions:
        bot.send_message(message.chat.id, msg ,reply_markup=markup)
    pass

# @bot.message_handler(regexp="/all_result")
# def all_result(message):
#     workbook = Workbook()
#     for i in range(10):
#         workbook.create_sheet(title="Number"+str(i))
#     workbook.save(filename='test')
#
#
#     pass

@bot.message_handler(regexp="/radushin")
def test(message):
    bot.send_document(message.chat.id,'/polling_bot/test.zip')
    pass

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data:
            # bot.answer_callback_query(call.id, text="Done!")
            # user_id = json.loads(call.message)[0]
            print(1)
            data = add_new_polling(call.message.chat.id,call.message.message_id,call.message.text)
            try:
                votes = data[0][3]
                summa = data[0][4]
            except:
                votes=0
                summa=0
            print('votes ' + str(votes))
            print('summa ' + str(summa))
            if user_is_new(call.message.message_id, call.from_user.id):
                new_summa = (int(votes)*float(summa) + int(call.data))/(int(votes)+1)
                add_vote(call.message.message_id,votes)
                new_sum(call.message.message_id,new_summa)
                bot.answer_callback_query(call.id, text=str(call.data))
            else:
                print(2)
                bot.answer_callback_query(call.id, text='Already voted')
    pass

@bot.message_handler(regexp="/result")
def get_result(message):
    query = """SELECT *
                	        FROM public.polls
                            WHERE chat_id={}
                            ORDER BY msg_id DESC
                            LIMIT 3;"""
    query_result = db_query.execute_query(query.format(message.chat.id))
    print(query_result.value)
    msg = """Текст сообщения: {} \n
    Количество ответов: {} \n
    Среднее значение: {} \n
            """
    for data in query_result.value:
        bot.send_message(message.chat.id, msg.format(data[5],data[3],data[4]))


@bot.message_handler(content_types='text')
def default_answer(message):
    # bot.send_message(message.chat.id, "You are not authorized")
    pass



while True:
    # bot.polling(none_stop=True)
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(e)
        time.sleep(15)