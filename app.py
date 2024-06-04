import json
from flask import Flask, request, jsonify, render_template, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

function_app_url = "http://ehb-chatbot.azurewebsites.net/api/ehbchatbot"  # Update this with the actual Azure function URL if deployed
API_KEY = os.getenv("AZURE_FUNCTION_API_KEY")

@app.route('/', methods=['GET'])
def home():
    session.pop('chat_history', None)  # Clear chat history on new session
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def ask():
    user_input = request.form['question']

    # Retrieve chat history from session
    chat_history = session.get('chat_history', [])

    # Add current question to chat history
    chat_history.append({"sender": "user", "message": user_input})

    # Limit chat history to the last 5 messages
    chat_history = chat_history[-5:]

    # Prepare payload for Azure Function
    payload = {
        "previousMessages": chat_history,
        "currentMessage": {"sender": "user", "message": user_input}
    }

    response = requests.post(function_app_url, json=payload)

    # Extract bot response and add to chat history
    bot_response = response.json().get('message')
    chat_history.append({"sender": "bot", "message": bot_response})

    # Save updated chat history back to session
    session['chat_history'] = chat_history

    return jsonify(bot_response)

if __name__ == '__main__':
    app.run(debug=True)
