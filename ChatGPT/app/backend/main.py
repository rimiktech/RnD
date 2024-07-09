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
    return jsonify(response)  


@app.post("/api/continue")
def continueExecution():
    print("Executed")
    userData = request.get_json()
    userQuery = userData.get('reply')
    question = userData.get('question')
    print("------------------------- Data recived--------------------------------------------")
    print("User Query: ", userQuery)
    print("Question : ", question)
    print("------------------------- Data recived--------------------------------------------")
    response = execute_query(question,userQuery)
    print(response)
    return jsonify(response) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
