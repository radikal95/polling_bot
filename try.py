from db_tool import DbQuery
import zipfile
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
temp_chat_name = ''
chat_names = []
for data in query_result.value:
    # print(data)
    # print(data[1])
    # print(bot.get_chat(data[1]).title)
    if temp_chat_name ==bot.get_chat(data[1]).title:

        continue
    else:
        chat_names.append(bot.get_chat(data[1]).title)
        workbook.create_sheet(bot.get_chat(data[1]).title)

        # temp_chat_name = bot.get_chat(data[1]).title
print(chat_names)

for name in chat_names:
    workbook.create_sheet(name)

workbook.save('test.xlsx')



z = zipfile.ZipFile('test.zip', 'w')
z.write('test.xlsx')
z.close()
