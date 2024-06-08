import json
import logging

from flask import Flask, request, jsonify, render_template, session
import requests
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

cors_anywhere_url = os.getenv('CORS_ANYWHERE_URL')
function_app_url = f"https://ehb-chatbot.azurewebsites.net/api/openai_request_function?code={os.getenv('AZURE_FUNCTION_API_KEY')}"


@app.route('/', methods=['GET'])
def home():
    session.pop('chat_history', None)  # Clear chat history on new session
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data['question']
    logging.info(f"User input: {user_input}")

    # Retrieve chat history from session
    chat_history = session.get('chat_history', [])
    logging.info(f"Chat history: {chat_history}")

    # Add current question to chat history
    chat_history.append({"sender": "user", "message": user_input})

    # Limit chat history to the last 5 messages
    chat_history = chat_history[-5:]

    # Prepare payload for Azure Function
    payload = {
        "previousMessages": chat_history,
        "currentMessage": {"sender": "user", "message": user_input}
    }
    logging.info(f"Payload: {payload}")

    request_url = cors_anywhere_url + function_app_url
    logging.info(f"Request URL: {request_url}")

    # Add the missing header
    response = requests.post(request_url, json=payload, headers={'Content-Type': 'application/json', 'x-requested-with': 'XMLHttpRequest'})
    logging.info(f"Response status code: {response.status_code}")
    logging.info(f"Response content: {response.content}")

    try:
        response_json = response.json()
    except json.JSONDecodeError:
        print("Failed to decode response content as JSON")
        response_json = {}

    # Extract bot response and add to chat history
    bot_response = response_json.get('message')
    chat_history.append({"sender": "bot", "message": bot_response})

    # Save updated chat history back to session
    session['chat_history'] = chat_history

    print(f"Bot response: {bot_response}")
    return jsonify({"message": bot_response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
