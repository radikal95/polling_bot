from db_tool import DbQuery
from openpyxl import Workbook
import config
import telebot

bot = telebot.TeleBot(config.token)

db_query = DbQuery()
workbook = Workbook()
query = """SELECT *
    	        FROM public.polls
    	        ORDER by chat_id ASC, id ASC;"""
query_result = db_query.execute_query(query)

for data in query_result.value:
    # print(data)
    # print(data[1])
    print(bot.get_chat(data[1]))
