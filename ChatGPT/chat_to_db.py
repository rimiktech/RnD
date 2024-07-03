import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
mysql_uri = os.getenv("mysql_uri")

print("Connecting to database...")
db = SQLDatabase.from_uri(mysql_uri)
print("Connected.")

llm = ChatOpenAI()

def get_schema(db):
    schema = db.get_table_info()
    return schema

schema = get_schema(db)

print(schema)
exit()
user_question = 'How many users are there?'

template = """You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only use the following tables:
{0}

Question: {1}"""

prompt = template.format(schema, user_question)

import pdb
pdb.set_trace()




print("hhh")
sql_chain = (RunnablePassthrough.assign(schema=get_schema) | prompt | llm.bind(stop=["\nSQLResult:"]) | StrOutputParser())

print("Creating SQL query...")
user_question = 'How many users are there?'
print(sql_chain.invoke({"question": user_question, "database":db}))

