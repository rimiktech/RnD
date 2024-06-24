import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

load_dotenv()
mysql_uri = os.getenv("mysql_uri")

print("Connecting to database...")
db = SQLDatabase.from_uri(mysql_uri)
print("Connected.")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

print("Creating SQL query...")
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
print("Created.")

print("Executing query...")
chain = write_query | execute_query
response = chain.invoke({"question": "How many users are there?"})
print(response)