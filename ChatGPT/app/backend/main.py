from flask import Flask, jsonify, request
from ai import run_conversation , execute_query_fn
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173","http://127.0.0.1:5500"])


@app.get("/test")
def test():
    return "Test route is working!"

@app.post("/api/chat")
def chat():
    userData = request.get_json()
    userQuery = userData.get('query')
    response = run_conversation(userQuery)
    return response


@app.post("/api/confirmQueryExecution")
def confirmQueryExecution():
    print("Executed")
    userData = request.get_json()
    userQuery = userData.get('reply')
    chat_message = userData.get('chat_message')
    function_name = userData.get('function_name')
    tool_call_type = userData.get('tool_call_type')
    tools = userData.get('tools')
    tool_call_id = userData.get('tool_call_id')
    tool_calls = [ChatCompletionMessageToolCall(id=tool_call_id, function=Function(arguments=f'{"query":${userQuery}}', name=function_name), type=tool_call_type)]
    response = execute_query_fn(messages = chat_message, tool_calls = tool_calls, query_to_execute =userQuery, tools = tools)
    print(response)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)