from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

AZURE_FUNCTION_URL = "http://localhost:7071/api/AskOpenAI"  # Update this with the actual Azure function URL if deployed
API_KEY = os.getenv("AZURE_FUNCTION_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "Welcome to my Flask app!"


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Verzend de vraag naar de Azure Function App
    response = send_question_to_azure_function(question)
    return jsonify(response)

def send_question_to_azure_function(question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "question": question
    }
    response = requests.post(AZURE_FUNCTION_URL, json=data, headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)