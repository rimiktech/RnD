import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
mysql_uri = os.getenv("mysql_uri")

template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""

prompt = ChatPromptTemplate.from_template(template)

print("Connecting to database...")
db = SQLDatabase.from_uri(mysql_uri)
print("Connected.")

def get_schema(input):
    schema = input['database'].get_table_info()
    return schema

llm = ChatOpenAI()

sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

print("Creating SQL query...")
user_question = 'How many users are there?'
print(sql_chain.invoke({"question": user_question, "database":db}))

