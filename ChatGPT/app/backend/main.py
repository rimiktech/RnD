from flask import Flask, jsonify, request
from ai import run_conversation, execute_query
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5500","http://192.168.29.172:3000"])


@app.get("/test")
def test():
    return "Test route is working!"

@app.post("/api/chat")
def chat():
    userData = request.get_json()
    userQuery = userData.get('query')
    response = run_conversation(userQuery)
    return  response


@app.post("/api/continue")
def continueExecution():
    print("Executed")
    
    userData = request.get_json()
    userQuery = userData.get('reply')
    question = userData.get('question')
    function_name = userData.get('function_name')
    function_args = userData.get('function_args')
    tools = userData.get('tools')
    messages = userData.get('messages')
    tool_calls = userData.get('tool_calls')
    tool_call_id = userData.get('tool_call_id')
    
    print("------------------------- Data recived--------------------------------------------")
    print("User Query: ", userQuery)
    print("Question : ", question)
    print("function_name : ", function_name)
    print("function_args : ", function_args)
    print("tools : ", tools)
    print("messages : ", messages)
    print("tool_calls : ", tool_calls)
    print("tool_call_id : ", tool_call_id)
    print("------------------------- Data recived--------------------------------------------")
 
    response = execute_query(question ,function_name,userQuery,tools,messages,tool_calls,tool_call_id)
    print(response)
    return jsonify(response) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
