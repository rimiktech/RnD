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

def run_query(query):
    print("Running following query:\n-> '{0}'".format(query))
    data = db.run(query)
    print("The query has been run successfully.")
    return data 

def get_schema():
    print("Getting schema of the database...")
    schema = db.get_table_info()
    print("Got the schema.")
    return schema

instructions = """
You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.

Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.

Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.

Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Pay attention to use date('now') function to get the current date, if the question involves "today". Please do not use double quotation marks (") for table names and column names when writing SQL queries. For example, instead of writing SELECT * FROM "user";, write SELECT * FROM user;.
Please refrain from using backslashes (\\) also while writing queries.

Question: 
{0}
"""

def run_conversation(user_query):
    print("User: {0}".format(user_query))
    prompt = instructions.format(user_query)
    messages = [{"role": "user", "content": "{0}".format(prompt)}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "run_query",
                "description": "Run any sql query to get the data from database",
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
                "description": "To get the schema of the database, that will help to write correct sql queries",
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

    if tool_calls:
        available_functions = {"run_query": run_query, "get_schema": get_schema}
        messages.append(response_message)

        while tool_calls:
            tool_call = tool_calls[0]  
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            
            if function_name == "run_query":
                function_response = function_to_call(query=function_args.get("query"))
            else:
                function_response = function_to_call()

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
            
            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            response_message = second_response.choices[0].message
            tool_calls = response_message.tool_calls
            messages.append(response_message)

        return response_message


# if __name__ == '__main__':
    # user_query = "Let me know the total number of clients?"

    # print("ChatGPT: "+run_conversation(user_query).content)


