import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from utilities.Database import SQLDatabase

load_dotenv()
mysql_uri = os.getenv("mysql_uri")

client = OpenAI()

print("Connecting database...")
db = SQLDatabase.from_uri(mysql_uri)
print("Connected.")

schema_cache = None

def run_query(query):
    print(f"Running following query:\n-> '{query}'")
    data = db.run(query)
    print("The query has been run successfully.")
    return data 

def get_schema():
    global schema_cache
    if schema_cache is not None:
        print("Schema already fetched. Using cached schema.")
        return schema_cache
    
    print("Getting schema of the database...")
    schema_cache = db.get_table_info()
    print("Got the schema.")
    return schema_cache

# get_schema()

instructions = """
You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.

Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.

Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.

Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Pay attention to use date('now') function to get the current date, if the question involves "today". Please do not use double quotation marks (") for table names and column names when writing SQL queries. For example, instead of writing SELECT * FROM "user";, write SELECT * FROM user;.

Please refrain from using backslashes (\) also while writing queries.

Do not fetch the schema again if you have already retrieved it once.

Question: 
{0}
"""

def run_conversation(user_query):
    print(f"User: {user_query}")
    prompt = instructions.format(user_query)
    messages = [{"role": "user", "content": prompt}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "run_query",
                "description": "Run any SQL query to get the data from the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The SQL query, e.g., SELECT count(*) FROM user;",
                        },
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_schema",
                "description": "To get the schema of the database, which will help to write correct SQL queries",
            },
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    tool_call = tool_calls[0]
    function_args = json.loads(tool_call.function.arguments)
    query = function_args.get("query")
    data = [{
        "query": query,
        "question":user_query
        
    }]
    print(data)
    return data


def execute_query(question , query_to_execute):
    execution_instruction = """
    The user question was {0} and output is {1} , restructure this the given output according to question
    """
    output = run_query(query_to_execute)
    
    prompt = execution_instruction.format(question, output)
    messages = [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print(response)

    return response.choices[0].message.content
# Example usage:
# if __name__ == '__main__':
#     user_query = "SELECT count(*) as user_count FROM user;"
#     print("ChatGPT: " + execute_query_fn("Let me know the number of users?",user_query))
