import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()
mysql_uri = os.getenv("mysql_uri")

print("Connecting to database...")
db = SQLDatabase.from_uri(mysql_uri)
print("Connected.")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
print(agent_executor.invoke({"input": "How many users are there?"}))