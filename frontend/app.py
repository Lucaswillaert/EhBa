import json
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

function_app_url = "http://ehb-chatbot.azurewebsites.net/api/ehbchatbot"  # Update this with the actual Azure function URL if deployed
API_KEY = os.getenv("AZURE_FUNCTION_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "Welcome to my Flask app!"


@app.route('/chat', methods=['POST'])
def ask():
    user_input = request.form['question']
    response = requests.post(function_app_url, json={"question" : user_input})
    return jsonify(response.text)

if __name__ == '__main__':
    app.run(debug=True)