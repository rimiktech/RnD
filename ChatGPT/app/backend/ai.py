import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from utilities.Database import SQLDatabase
import uuid

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

execution_details = [{
    "uid" : "",
    "messages":""
}]

# get_schema()

instructions = """
You are a MySQL expert. If the user's question is general and not related to the database, provide an appropriate response. If the question is related to the database, first fetch the schema to understand the structure, then create a syntactically correct MySQL query to run based on the schema instructions, and provide the query to the user.

Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause. You can order the results to return the most informative data in the database.

Never query for all columns from a table. You must query only the columns that are needed to answer the question. Use only the column names you can see in the tables. Be careful not to query columns that do not exist. Also, ensure you know which column is in which table.

Use the CURRENT_DATE function to get the current date if the question involves "today". Do not use double quotation marks (") or backslashes (\) when writing SQL queries.

And Your name is RnD
Question: 
{0}

"""

def run_conversation(user_query):
    print(f"User: {user_query}")
    prompt = instructions.format(user_query)
    actual_message = [{"role": "user", "content": prompt}]
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
    print("----------------------This is First Response -------------------")
    print(response)
    response_message = response.choices[0].message
    print(response_message)
    tool_calls = response_message.tool_calls
    print(tool_calls)
    if tool_calls:
        available_functions = {"run_query": run_query, "get_schema": get_schema}
        messages.append(response_message)

        while tool_calls:
            tool_call = tool_calls[0]  
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            
            if function_name == "run_query":
                query = function_args.get("query")
                
                uid = str(uuid.uuid4())
                global execution_details
                appendData = {
                  "uid": uid,
                  "messages" : messages  
                }
                execution_details.append(appendData)
                data = [{
                    "query": query,
                    "question":user_query,
                    "function_name" : function_name,
                    "answer":None,
                    "uid":uid,
                    "tools":tools,
                    "tool_calls": True,
                    "tool_call_id":tool_call.id
                }]
                print("----------------Run Query -----------------")
                print(data)
                return data
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
        data = [{
                    "query": None,
                    "question":user_query,
                    "function_name" : None,
                    "answer": response_message.content,
                    "tools":None,
                    "uid": None,
                    "messages":None,
                    "tool_calls": False,
                    "tool_call_id":None
                }]
        print(data)
        print("----------------After Schema Called -----------------")
        print(data)   
        return data
    
    data = [{
                    "query": None,
                    "question":user_query,
                    "function_name" : None,
                    "answer": response_message.content,
                    "tools":None,
                    "uid": None,
                    "messages":None,
                    "tool_calls": False,
                    "tool_call_id":None
                }]
    print(data)
    print("---------------General Question-----------------")
    print(data)   
    return data


def execute_query(question ,function_name,function_args,tools,uid,tool_calls,tool_call_id):
    global execution_details
    messages = ""
    
    print(execution_details)
    for detail in execution_details:
        if detail["uid"] == uid:
            messages = detail["messages"]
    print(messages)
    if tool_calls:
        available_functions = {"run_query": run_query, "get_schema": get_schema}
        
        while tool_calls:
            function_to_call = available_functions[function_name]  
            
            if function_name == "run_query":
                function_response = function_to_call(query=function_args)
            else:
                function_response = function_to_call()

            messages.append(
                {
                    "tool_call_id": tool_call_id,
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
            if(response_message.tool_calls):
                tool_calls = response_message.tool_calls
                tool_call = tool_calls[0]  
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                tool_calls = True
            else:
                tool_calls=False
                
            messages.append(response_message)
            
        data = [{
                    "query": None,
                    "question":question,
                    "function_name" : None,
                    "answer": response_message.content,
                    "tools":None,
                    "messages":None,
                    "uid":None,
                    "tool_calls": False,
                    "tool_call_id":None
                }]
        # for detail in execution_details:
        #     if detail["uid"] == uid:
        #         execution_details.pop(detail)
                
        print("--------------Final output to user --------------")
        print(data)
        return data
    
# Example usage:
# if __name__ == '__main__':
#     user_query = "SELECT count(*) as user_count FROM user;"
#     print("ChatGPT: " + execute_query_fn("Let me know the number of users?",user_query))
