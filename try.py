from db_tool import DbQuery
from openpyxl import Workbook

db_query = DbQuery()
workbook = Workbook()
query = """SELECT *
    	        FROM public.polls
    	        ORDER by chat_id ASC, id ASC;"""
query_result = db_query.execute_query(query)

for i in range(10):
    workbook.create_sheet(title="Number"+str(i))
workbook.save(filename='test.xlsx')