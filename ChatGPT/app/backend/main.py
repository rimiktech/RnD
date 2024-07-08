from flask import Flask, jsonify, request
from chat_to_db1 import run_conversation
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
    response = run_conversation(userQuery).content
    print(response)
    return response

if __name__ == '__main__':
      app.run(debug=True)